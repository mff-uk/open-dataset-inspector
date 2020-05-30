#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple, defaultdict
from dataclasses import dataclass

import typing
import json
import itertools

HierarchyEntry = namedtuple("hierarchy", ["source", "type", "target"])


@dataclass
class MappingItem:
    entity: str
    metadata: object


@dataclass
class Mapping:
    id: str
    metadata: object
    data: typing.List[MappingItem]


@dataclass
class Dataset:
    id: str
    mappings: typing.List[Mapping]
    hierarchy: typing.List[HierarchyEntry]


AdjacencyList = typing.Dict[str, typing.Set[str]]


@dataclass
class Path:
    """Node int he middle of the path."""
    shared: str
    """Path with start/end and the start and end respectively."""
    nodes: typing.Tuple[str]

    def __hash__(self):
        return hash(self.shared) + hash(self.nodes)

    def __eq__(self, other):
        return self.shared == other.shared and self.nodes == other.nodes


def main():
    left = _load_dataset_from_file("../data/mapping/v1/000005.json")
    right = _load_dataset_from_file("../data/mapping/v1/000049.json")
    all_paths = find_all_path(left, right)
    closest_paths = select_closest_for_each(all_paths, {"distance": 3})
    print(json.dumps(paths_to_output(
        closest_paths, [left, right]), indent=2)
    )


def _load_dataset_from_file(file: str) -> Dataset:
    with open(file, encoding="utf-8") as stream:
        content = json.load(stream)
    return load_dataset_from_json(content)


def load_dataset_from_json(content) -> Dataset:
    mappings = [
        Mapping(item["metadata"]["from"], item["metadata"], [
            MappingItem(dataItem["id"], dataItem["metadata"])
            for dataItem in item["data"]
        ])
        for item in content["mappings"]
    ]
    hierarchy = [
        HierarchyEntry(item[0], item[1], item[2])
        for item in content["hierarchy"]
    ]
    return Dataset(content["@id"], mappings, hierarchy)


# region Collect paths

def find_all_path(left: Dataset, right: Dataset) -> typing.List[Path]:
    adjacency_list = _prepare_adjacency_list(
        [left.hierarchy, right.hierarchy])
    result = []
    for left_entry in _collect_entries(left):
        for right_entry in _collect_entries(right):
            result.extend(_find_path(adjacency_list, left_entry, right_entry))
    return result


def _collect_entries(dataset: Dataset):
    return list({
        item.entity
        for mapping in dataset.mappings
        for item in mapping.data
    })


def _prepare_adjacency_list(
        hierarchies: typing.List[typing.List[HierarchyEntry]]) \
        -> AdjacencyList:
    """Adjacency matrix target to source."""
    edges: typing.Set[HierarchyEntry] = set(itertools.chain(*hierarchies))
    result = {}
    for edge in edges:
        adjacency_list = result.get(edge.source, set())
        adjacency_list.add(edge.target)
        result[edge.source] = adjacency_list
    return result


def _find_path(
        adjacency_list: AdjacencyList, left: str, right: str) \
        -> typing.List[Path]:
    if left == right:
        return [Path(left, tuple([left]))]
    left_visited = {left}
    left_level = {left}
    right_visited = {right}
    right_level = {right}
    paths = {left: [left], right: [right]}

    def expand_level(l, r):
        return _expand_level(adjacency_list, paths, l, r)

    while True:
        left_level, left_paths = expand_level(left_visited, left_level)
        right_level, right_paths = expand_level(right_visited, right_level)
        # Check for intersections - i.e. if we have found the path.
        intersection = set().union(
            left_level.intersection(right_visited),
            left_level.intersection(right_level),
            right_level.intersection(left_visited),
            right_level.intersection(left_level),
        )
        if len(intersection) > 0:
            result: typing.List[Path] = []
            for shared in intersection:
                left_shared = left_paths.get(shared, paths.get(shared))
                right_shared = right_paths.get(shared, paths.get(shared))
                right_shared.reverse()
                path = tuple(left_shared + right_shared[1:])
                result.append(Path(shared, path))
            return result
        paths.update(left_paths)
        paths.update(right_paths)
        # Filter out already visited.
        left_visited.update(left_level)
        right_visited.update(right_level)
        # Check for end of the iteration.
        if not left_level and not right_level:
            break
    # No path found.
    return []


def _expand_level(
        adjacency_list: AdjacencyList,
        paths: typing.Dict[str, typing.List[str]],
        visited: typing.Set[str],
        level: typing.Set[str]):
    new_nodes = set()
    new_paths = {}
    for source in level:
        for target in adjacency_list.get(source, []):
            if target in visited:
                continue
            new_nodes.add(target)
            #
            path = paths[source].copy()
            path.append(target)
            new_paths[target] = path
    return new_nodes, new_paths


# endregion

def paths_to_output(
        paths: typing.List[Path], datasets: typing.List[Dataset],
        metadata: typing.Dict = None):
    path_lengths = [len(path.nodes) for path in paths]

    if metadata is None:
        metadata = {}

    similarity = { }
    if path_lengths:
        similarity["max"] = max(path_lengths)
        similarity["average"] = sum(path_lengths) / len(path_lengths)
        similarity["sum"] = sum(path_lengths)
        similarity["min"] = min(path_lengths)

    return {
        "metadata": {
            **metadata,
            "datasets": [dataset.id for dataset in datasets],
        },
        "similarity": similarity,
        "paths": [
            {
                "shared": path.shared,
                "nodes": path.nodes,
            } for path in paths
        ]
    }


# region Path filters and selectors

def select_paths_by_length(paths: typing.List[Path], options) \
        -> typing.List[Path]:
    """Return all paths shorted than given threshold."""
    # Two neighbouring nodes have paths of size 2 so we add 2 to make
    # 0 stand for two nodes next to each other.
    max_length = options.get("distance", 0) + 2
    return [path for path in paths if len(path.nodes) <= max_length]


def select_closest_for_each(paths: typing.List[Path], options: any = None) \
        -> typing.List[Path]:
    """
    For each entity in left and right choose the closes element from the other
    set.
    """
    shortest_paths: typing.Dict[str, Path] = {}

    def update_shortest(item: str, new_path: Path):
        if item not in shortest_paths:
            shortest_paths[item] = new_path
        elif len(shortest_paths[item].nodes) > len(new_path.nodes):
            shortest_paths[item] = new_path

    for path in paths:
        update_shortest(path.nodes[0], path)
        update_shortest(path.nodes[-1], path)

    unique_paths = list(set(shortest_paths.values()))

    if "distance" in options:
        unique_paths = select_paths_by_length(unique_paths, options)

    return unique_paths


# endregion

if __name__ == "__main__":
    main()
