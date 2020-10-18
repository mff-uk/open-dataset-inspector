#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
import typing
from dataclasses import dataclass
import collections
import itertools
import shutil

from glib.input_output import write_json, read_json, logger
from glib.workflow import \
    AbstractTransformation, \
    TransformationContext, \
    AbstractParallelTransformation, \
    TransformationChunk


# region AddFromJsonLines

class AddFromJsonLines(AbstractTransformation):

    def __init__(self, input_file: str, data_selector):
        self._input_file = input_file
        self._data_selector = data_selector

    def __call__(self, input_dir: str, output_dir: str):
        with TransformationContext(output_dir) as context:
            for new_content in self._iterate_input_file():
                path = context.get_or_create(new_content["iri"])
                old_content = {}
                if os.path.exists(path):
                    old_content = read_json(path)
                write_json(path, self._data_selector(old_content, new_content))

    def _iterate_input_file(self):
        with open(self._input_file, encoding="utf-8") as stream:
            for line in stream:
                yield json.loads(line)


# endregion

# region AddWikidataMapping

@dataclass
class WikidataMappingSelectorResult:
    """From entity select data used for mapping."""
    get: typing.Callable[[None], typing.List[typing.List[str]]]
    """Create result mapping entry record. Return None to ignore mapping."""
    create: typing.Callable[[str, str, str], typing.Optional[object]]
    """Set mapping to entity."""
    set: typing.Callable[[object], None]


WikidataMappingSelector = \
    typing.Callable[[any], typing.List[WikidataMappingSelectorResult]]


@dataclass
class WikidataMappingContext:
    wikidata_file: str
    allowed_distance: int
    shared_threshold: float
    # Filter out terms that are not used for mapping.
    words_filter: typing.Callable[[typing.List[str]], typing.List[str]]
    # Filter out terms that can not be used for mapping if they are alone.
    shared_words_filter: typing.Callable[[typing.List[str]], typing.List[str]]
    # Read/create/write data related to mapping.
    mapping_selector: WikidataMappingSelector


class AddWikidataMapping(AbstractParallelTransformation):
    """
    We require the wikidata entity to be in the given text, for
    entity "A B C" and text "0 A B C 1" we got match, but also
    with "0 A 1 B 2 C" or "C B A".
    """

    def __init__(
            self, chunk_count, thread_count,
            context: WikidataMappingContext):
        super().__init__(chunk_count, thread_count)
        self._context = context

    def get_worker(self) -> typing.Callable[[TransformationChunk], None]:
        return AddWikidataMappingWorker()

    def get_context(self):
        return self._context


@dataclass
class WikidataEntity:
    code: str
    label: typing.List[str]
    alias: typing.List[typing.List[str]]

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code


WikidataEntityMap = typing.Dict[str, typing.List[WikidataEntity]]


class AddWikidataMappingWorker:
    _context: WikidataMappingContext

    def __call__(self, chunk: TransformationChunk):
        self._tasks = chunk.tasks
        self._context = chunk.context
        #
        logger.info("Loading terms for %i entities", len(chunk.tasks))
        terms = self._collect_terms()
        logger.info("Terms count %i", len(terms))
        logger.info("Mapping to labels ...")
        terms_to_entities = self._map_terms_to_wikidata(terms)
        logger.info("Saving mappings ...")
        self._write_terms_mapping(terms_to_entities)

    def _collect_terms(self):
        result = set()
        for task in self._tasks:
            data = read_json(task.in_path)
            for selector in self._context.mapping_selector(data):
                result.update({
                    word
                    for item in selector.get()
                    for word in item
                })
        return self._context.words_filter(list(result))

    def _map_terms_to_wikidata(self, terms) -> WikidataEntityMap:
        # First we collect mapping from terms to entities ID and
        # we save all found entities.
        # Then we replace the entity ID with the entities at the end.
        terms_to_entities = collections.defaultdict(list)
        entities = {}
        for index, (entity_id, entity) in enumerate(self._iterate_labels()):
            search_label = self._get_search_label(entity)
            search_alias = self._get_search_alias(entity)
            search_alias_terms = [
                term
                for terms in search_alias
                for term in terms
            ]

            entity_has_mapped = False
            for search_term in (set(search_label) | set(search_alias_terms)):
                if search_term not in terms:
                    continue
                # Given term is in the Wikidata entity text.
                if entity_id not in terms_to_entities[search_term]:
                    terms_to_entities[search_term].append(entity_id)
                entity_has_mapped = True

            if entity_has_mapped:
                entities[entity_id] = \
                    WikidataEntity(entity_id, search_label, search_alias)

            if index % 100000 == 0:
                logger.info("  {:>7}".format(index))

        return {
            key: [entities[entity_id] for entity_id in values]
            for key, values in terms_to_entities.items()
        }

    def _iterate_labels(self):
        with open(self._context.wikidata_file, encoding="utf8") as in_stream:
            for line in in_stream:
                data = json.loads(line)
                yield data["id"], data

    def _get_search_label(self, entity):
        if "label" not in entity:
            return []
        return self._context.words_filter([
            item for item in entity["label"]])

    def _get_search_alias(self, entity):
        if "aliases" not in entity:
            return []
        return [self._context.words_filter(item) for item in entity["aliases"]]

    def _write_terms_mapping(self, terms_to_entities: WikidataEntityMap):
        log_progress_step = max(1, int(len(self._tasks) / 20.0))

        io_time = 0
        working_time = 0

        for index, task in enumerate(self._tasks):
            if index % log_progress_step == 0:
                logger.info(
                    "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                        index, len(self._tasks), io_time, working_time))
            io_time_start = time.time()
            entity = read_json(task.in_path)
            io_time += time.time() - io_time_start

            working_time_start = time.time()
            for selector in self._context.mapping_selector(entity):
                self._add_mappings_for_selector(selector, terms_to_entities)
            working_time += time.time() - working_time_start

            io_time_start = time.time()
            write_json(task.out_path, entity)
            io_time += time.time() - io_time_start

        logger.info(
            "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                len(self._tasks), len(self._tasks), io_time, working_time))

    def _add_mappings_for_selector(
            self,
            selector: WikidataMappingSelectorResult,
            terms_to_entities: WikidataEntityMap):
        mappings = [
            mapping
            for terms in selector.get()
            for mapping in self._collect_mapping_for_terms(
                terms, selector, terms_to_entities)
        ]
        selector.set(mappings)

    def _collect_mapping_for_terms(
            self,
            terms: typing.List[str],
            selector: WikidataMappingSelectorResult,
            terms_to_entities: WikidataEntityMap
    ) -> typing.List:
        """Return all mappings for given terms."""
        filtered_terms = self._context.words_filter(terms)
        # For each entity collect all shared terms.
        mapped_to: typing.Dict[WikidataEntity, typing.List[str]] = \
            collections.defaultdict(list)
        for term in filtered_terms:
            for entity in terms_to_entities.get(term, []):
                mapped_to[entity].append(term)
        result = []
        # For each entity create mapping.
        for wikidata_entity, mapped_by in mapped_to.items():
            mapping = self._create_mapping_for_entity(
                selector, filtered_terms, wikidata_entity, mapped_by)
            if mapping is not None:
                result.append(mapping)
        return result

    def _create_mapping_for_entity(
            self,
            selector: WikidataMappingSelectorResult,
            terms: typing.List[str],
            wikidata: WikidataEntity,
            mapped_by: typing.List[str]
    ):
        """
        :param terms: All dataset terms.
        :param wikidata: Wikidata entity.
        :param mapped_by: Terms shared with the entity.
        :return:
        """
        max_shared = []
        max_target = []
        max_threshold = 0
        for wikidata_terms in itertools.chain([wikidata.label], wikidata.alias):
            if len(wikidata_terms) == 0:
                continue
            max_shared_estimate = list(set(wikidata_terms) & set(mapped_by))
            if len(self._context.shared_words_filter(max_shared_estimate)) == 0:
                # Mapping is based only on words that should not be shared alone.
                continue
            threshold_estimate = \
                float(len(max_shared_estimate)) / len(wikidata_terms)
            if threshold_estimate < self._context.shared_threshold:
                # The size of shared is under the threshold.
                continue
            if threshold_estimate < max_threshold:
                # We already have better match.
                continue
            if len(wikidata_terms) < len(max_shared):
                # We already have match bigger than this one can ever be.
                continue
            # Check for 100% match, as many Wikidata labels
            # are short
            if len(wikidata_terms) == len(mapped_by):
                if len(wikidata_terms) > len(max_shared):
                    max_shared = wikidata_terms
                    max_target = wikidata_terms
                    max_threshold = 1.0
                continue
            # There is partial match, for now we just take that.
            # TODO Improve tha matching here.
            max_shared = max_shared_estimate
            max_target = wikidata_terms
            max_threshold = threshold_estimate

        if len(max_shared) == 0:
            return None

        return selector.create(wikidata.code, max_shared, max_target)


# endregion

# region AddWikidataHierarchy

@dataclass
class AddWikidataHierarchyContext:
    hierarchy_file: str
    mapping_selector: typing.Callable[[any], typing.Generator[str, None, None]]
    set_hierarchy: typing.Callable[[any, typing.List], None]


class AddWikidataHierarchy(AbstractParallelTransformation):

    def __init__(
            self, chunk_count, thread_count,
            context: AddWikidataHierarchyContext):
        super().__init__(chunk_count, thread_count)
        self._context = context

    def get_worker(self) -> typing.Callable[[TransformationChunk], None]:
        return AddWikidataHierarchyWorker()

    def get_context(self):
        return self._context


class AddWikidataHierarchyWorker:
    _context: AddWikidataHierarchyContext

    def __call__(self, chunk: TransformationChunk):
        self._tasks = chunk.tasks
        self._context = chunk.context
        #
        logger.info("Loading individuals for: %i tasks", len(self._tasks))
        entities = self._collect_mapped_to()
        logger.info("Collecting hierarchy for: %i entities", len(entities))
        hierarchy = self._collect_hierarchy(entities)
        logger.info("Hierarchy size: %i", len(hierarchy))
        self._save_hierarchy(hierarchy)

    def _collect_mapped_to(self):
        result = set()

        io_time = 0
        working_time = 0
        log_step = max(1, int(len(self._tasks) / 20.0))
        for index, task in enumerate(self._tasks):
            if index % log_step == 0:
                logger.info(
                    "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                        index, len(self._tasks), io_time, working_time))

            io_start = time.time()
            entity = read_json(task.in_path)
            io_time += time.time() - io_start

            work_start = time.time()
            for mapped_to in self._iter_mapped_to_for_entity(entity):
                result.add(mapped_to)
            working_time += time.time() - work_start

        logger.info(
            "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                len(self._tasks), len(self._tasks), io_time, working_time))

        return result

    def _iter_mapped_to_for_entity(self, entity):
        for mapping in self._context.mapping_selector(entity):
            yield mapping

    def _collect_hierarchy(self, entities):
        to_resolve = set(entities)
        resolved = {}

        while len(to_resolve) > 0:
            logger.info("  Iterating hierarchy file with %i entries",
                        len(to_resolve))
            last_size = len(to_resolve)
            for line in self._iterate_json_lines(self._context.hierarchy_file):
                line_id = self._extract_id_from_line(line)
                if line_id not in to_resolve:
                    continue
                line_entry = self._line_to_entry(line)
                to_resolve.remove(line_id)
                resolved[line_id] = {
                    "instanceof": [
                        item for item in line_entry["instanceof"]],
                    "subclassof": [
                        item for item in line_entry["subclassof"]]
                }
                # Add new entities to resolve, if they have not been already
                # resolved. We also try to follow subclassof as a primary
                # source using instanceof only as a backup.
                if line_entry["subclassof"]:
                    to_resolve.update([
                        item
                        for item in line_entry["subclassof"]
                        if item not in resolved])
                else:
                    to_resolve.update([
                        item
                        for item in line_entry["instanceof"]
                        if item not in resolved])

            if last_size == 1 and len(to_resolve) == last_size:
                logger.info("Missing record for: ")
                for item in to_resolve:
                    resolved[item] = {
                        "instanceof": [],
                        "subclassof": [],
                        "type": "not-found"
                    }
                    logger.info("Missing record for: %s", item)
                break

        return resolved

    @staticmethod
    def _iterate_json_lines(path):
        with open(path, encoding="utf-8") as in_stream:
            for line in in_stream:
                yield line

    @staticmethod
    def _line_to_entry(line):
        line_entry = json.loads(line)
        return {
            "id": line_entry["id"],
            "instanceof": [
                item for item in line_entry.get("instanceof", [])],
            "subclassof": [
                item for item in line_entry.get("subclassof", [])]
        }

    @staticmethod
    def _extract_id_from_line(line):
        line_id = line[line.index('"id":') + 7:]
        line_id = line_id[:line_id.find('"')]
        return line_id

    def _save_hierarchy(self, hierarchy):
        logger.info("Saving hierarchy ...")

        io_time = 0
        working_time = 0

        log_step = max(1, int(len(self._tasks) / 20.0))
        for index, task in enumerate(self._tasks):
            if index % int(len(self._tasks) / log_step) == 0:
                logger.info(
                    "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                        index, len(self._tasks), io_time, working_time))

            io_start = time.time()
            entity = read_json(task.in_path)
            io_time += time.time() - io_start

            add_time = time.time()
            self._add_hierarchy(entity, hierarchy)
            working_time += time.time() - add_time

            io_start = time.time()
            write_json(task.out_path, entity)
            io_time += time.time() - io_start

        logger.info(
            "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                len(self._tasks), len(self._tasks), io_time, working_time))

    def _add_hierarchy(self, entity, hierarchy):
        to_resolve = set()
        for mapped_to in self._iter_mapped_to_for_entity(entity):
            to_resolve.add(mapped_to)

        resolved = set()
        relevant_hierarchy = set()
        while to_resolve:
            id_to_resolve = to_resolve.pop()
            resolved.add(id_to_resolve)
            assert id_to_resolve in hierarchy, \
                "Missing ID in hierarchy:" + id_to_resolve

            item = hierarchy[id_to_resolve]

            if item["subclassof"]:
                for parent in item["subclassof"]:
                    if parent not in resolved:
                        to_resolve.add(parent)
                    relevant_hierarchy.add(
                        (id_to_resolve, "subclass", parent))
                # If there are "subclassof" we do not store "instanceof"
                continue

            for parent in item["instanceof"]:
                if parent not in resolved:
                    to_resolve.add(parent)
                relevant_hierarchy.add(
                    (id_to_resolve, "instanceof", parent))

        self._context.set_hierarchy(entity, list(relevant_hierarchy))


# endregion

# region ReduceMapping

@dataclass
class ReduceMappingSelectorResult:
    # Return list of mappings.
    get: typing.Callable[[None], typing.List]
    # Set list of mappings.
    set: typing.Callable[[typing.List], None]


# For given type of mapping create a selector.
ReduceMappingSelector = \
    typing.Callable[[any], typing.List[ReduceMappingSelectorResult]]


@dataclass
class ReduceMappingContext:
    mapping_selector: ReduceMappingSelector
    hierarchy_selector: typing.Callable[[any], typing.List]
    # Create new entity with given mapping.
    create_mapped_entity: typing.Callable[[any, str], any]
    # Merge data from given entities.
    merge_entities: typing.Callable[[any, any, str], any]
    # Alternative of create_mapped_entity for non-mapped entities.
    create_originally_mapped: typing.Callable[[any], any]


class ReduceMapping(AbstractParallelTransformation):

    def __init__(
            self, chunk_count, thread_count,
            context: ReduceMappingContext):
        super().__init__(chunk_count, thread_count)
        self._context = context

    def get_worker(self) -> typing.Callable[[TransformationChunk], None]:
        return ReduceMappingWorker()

    def get_context(self):
        return self._context


class ReduceMappingWorker:
    _context: ReduceMappingContext

    def __call__(self, chunk: TransformationChunk):
        self._tasks = chunk.tasks
        self._context = chunk.context
        #
        io_time = 0
        working_time = 0
        log_step = max(1, int(len(self._tasks) / 20.0))
        for index, task in enumerate(self._tasks):
            if index % log_step == 0:
                logger.info(
                    "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                        index, len(self._tasks), io_time, working_time))

            io_start = time.time()
            entity = read_json(task.in_path)
            io_time += time.time() - io_start

            work_start = time.time()
            self._reduce_hierarchy_for_entity(entity)
            working_time += time.time() - work_start

            io_start = time.time()
            write_json(task.out_path, entity)
            io_time += time.time() - io_start

        logger.info(
            "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                len(self._tasks), len(self._tasks), io_time, working_time))

    def _reduce_hierarchy_for_entity(self, entity):
        reduce_map = self._load_reduce_map(entity)
        for selector in self._context.mapping_selector(entity):
            mappings = selector.get()
            new_value = self._reduce_hierarchy_for_mapping(
                reduce_map, mappings)
            selector.set(new_value)

    def _load_reduce_map(self, entity):
        """Return map that map wikidata elements to their reduced elements."""
        mapping = collections.defaultdict(set)
        hierarchy = self._context.hierarchy_selector(entity)
        for (source, prop_name, target) in hierarchy:
            if not prop_name == "instanceof":
                continue
            mapping[source].add(target)
        # Apply transitive mapping, i.e. A -> B, B -> C change to A -> C
        keys = list(mapping.keys())
        while True:
            has_changed = False
            for key in keys:
                to_update = {
                    value for value in mapping[key] if value in mapping
                }
                to_add = {
                    new_value
                    for value in to_update
                    for new_value in mapping[value]
                }
                # When we can only remove and not add then we are on the end
                # of instanceOf chan.
                if len(to_add) == 0:
                    continue
                has_changed = True
                mapping[key] = (mapping[key] | to_add) - to_update
            if not has_changed:
                break
        return dict(mapping)

    def _reduce_hierarchy_for_mapping(
            self,
            reduce_map: typing.Dict[str, typing.List[str]],
            mappings: typing.List[typing.Dict]):
        """
        For every mapping we check where does it maps to, some entities
        may have no mapping other can have multiple mappings.
        """
        result = {}
        context = self._context
        for mapping in mappings:
            source_id = mapping["id"]
            mapped_to = self._find_mappings(source_id, reduce_map)
            # Mapped to will also contains mapping to source_id,
            # thus we can simply iterate.
            for target_id in mapped_to:
                if target_id == source_id:
                    # Map to it self, so there is no mapping.
                    mapping = context.create_originally_mapped(mapping)
                else:
                    # Map to other item.
                    mapping = context.create_mapped_entity(mapping, target_id)
                # Add to result.
                if target_id in result:
                    # There is already a value for given ID, so we merge them.
                    result[target_id] = context.merge_entities(
                        mapping, result[target_id], target_id)
                else:
                    # There is no record for given ID we can just store the
                    # data.
                    result[target_id] = mapping
        return list(result.values())

    @staticmethod
    def _find_mappings(
            wikidata_id: str,
            reduce_map: typing.Dict[str, typing.List[str]]) \
            -> typing.List[str]:
        """Single entity can map to multiple values."""
        for_expansion = {wikidata_id}
        result = set()
        while for_expansion:
            next_to_expand = for_expansion.pop()
            if next_to_expand in result:
                continue
            if next_to_expand in reduce_map:
                for_expansion.update(reduce_map[next_to_expand])
            else:
                result.add(next_to_expand)
        return [x for x in result]


# endregion

# region Prune-mapped to

@dataclass
class PruneHierarchyContext:
    # Return list of all mappings.
    get_hierarchy: typing.Callable[[any], typing.List]
    set_hierarchy: typing.Callable[[any, typing.List], None]
    get_entities_to_remove: typing.Callable[[any], typing.Generator[str, None, None]]


class PruneHierarchy(AbstractParallelTransformation):
    """Remove entities from hierarchy."""

    def __init__(
            self, chunk_count, thread_count,
            context: PruneHierarchyContext):
        super().__init__(chunk_count, thread_count)
        self._context = context

    def get_worker(self) -> typing.Callable[[TransformationChunk], None]:
        return PruneHierarchyWorker()

    def get_context(self):
        return self._context


class PruneHierarchyWorker:
    _context: PruneHierarchyContext

    def __call__(self, chunk: TransformationChunk):
        self._tasks = chunk.tasks
        self._context = chunk.context
        #
        io_time = 0
        working_time = 0
        log_step = max(1, int(len(self._tasks) / 20.0))
        for index, task in enumerate(self._tasks):
            if index % log_step == 0:
                logger.info(
                    "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                        index, len(self._tasks), io_time, working_time))

            io_start = time.time()
            entity = read_json(task.in_path)
            io_time += time.time() - io_start

            work_start = time.time()
            self._prune_hierarchy(entity)
            working_time += time.time() - work_start

            io_start = time.time()
            write_json(task.out_path, entity)
            io_time += time.time() - io_start

        logger.info(
            "  {:>5} / {}   io: {:0.0f}s working: {:0.0f}s".format(
                len(self._tasks), len(self._tasks), io_time, working_time))

    def _prune_hierarchy(self, entity):
        to_remove = {item for item in self._context.get_entities_to_remove(entity)}
        hierarchy = [
            item
            for item in self._context.get_hierarchy(entity)
            # Remove all edges related to items to be removed.
            if item[0] not in to_remove and item[2] not in to_remove
        ]
        self._context.set_hierarchy(entity, hierarchy)


# endregion

# region ExportForUI

class ExportForUI(AbstractTransformation):

    def __init__(self, dataset_to_file_name_file: str):
        self._dataset_to_file_name_file = dataset_to_file_name_file

    def __call__(self, input_dir: str, output_dir: str):
        iri_to_file_name = read_json(self._dataset_to_file_name_file)
        with TransformationContext(input_dir, write_on_exit=False) as context:
            for task in context.iterate():
                assert task.iri in iri_to_file_name
                output_file_name = iri_to_file_name[task.iri]
                output_path = os.path.join(
                    output_dir, output_file_name + ".json")
                shutil.copyfile(task.path, output_path)


# endregion

def dict_get(target, name, default):
    path = name.split(".")
    for key in path[:-1]:
        if key not in target:
            return default
        target = target[key]
    return target.get(path[-1], default)


def dict_set(target, name, value):
    path = name.split(".")
    for key in path[:-1]:
        if key not in target:
            target[key] = {}
        target = target[key]
    target[path[-1]] = value
