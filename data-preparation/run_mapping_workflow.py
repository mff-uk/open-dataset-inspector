#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Execute main mapping workflow used to map datasets on Wikidata entries.
#
# Requires data produced by:
# * run_prepare_data_gov_cz.py
# * run_prepare_texts.py
#

import functools
import multiprocessing

from glib.workflow import Pipeline
from glib.workflow_tasks import *


def main():
    pipeline = Pipeline("../data/working")

    pipeline.directory("v1-00-input") \
        .apply(AddFromJsonLines
               ("../data/www.data.gov.cz/2020.04.20-www.data.gov.cz.jsonl",
                add_metadata_selector)) \
        .apply(AddFromJsonLines
               ("../data/www.data.gov.cz/2020.04.20-www.data.gov.cz.v3.jsonl",
                add_for_mapping_selector)) \
        .directory("v1-01-mapping") \
        .apply(AddWikidataMapping
               (4, 4,
                WikidataMappingContext(
                    "../data/www.wikidata.org/wikidata-cs.v3.jsonl",
                    2, 0.66,
                    no_stop_words_filter,
                    invalid_standalone_mapping_terms_filter,
                    mapping_selector
                ))) \
        .directory("v1-02-hierarchy") \
        .apply(AddWikidataHierarchy
               (4, 4,
                AddWikidataHierarchyContext(
                    "../data/www.wikidata.org/wikidata-hierarchy.jsonl",
                    mapping_for_hierarchy_selector,
                    set_hierarchy,
                )))

    pipeline.directory("v1-03-reduced-hierarchy") \
        .apply(ReduceMapping
               (4, 4,
                ReduceMappingContext(
                    mapping_selector, get_hierarchy,
                    create_mapped_entity, merge_mappings,
                    create_originally_mapped
                )))

    pipeline.directory("v1-04-prune-hierarchy") \
        .apply(PruneHierarchy
               (1, 1,
                PruneHierarchyContext(
                    get_hierarchy,
                    set_hierarchy,
                    get_reduced_from
                )))

    pipeline.directory("v1") \
        .apply(ExportForUI("../data/dataset-iri-to-file-name.json")) \

    pipeline.execute()


def add_metadata_selector(old, new):
    return {
        "@id": new["iri"],
        "metadata": {
            "title": new["title"],
            "description": new["description"],
            "keywords": new["keywords"],
        }
    }


def add_for_mapping_selector(old, new):
    return {
        **old,
        "mappings-value": {
            "title": new["title"],
            "description": new["description"],
            "keywords": new["keywords"],
        }
    }


# https://countwordsfree.com/stopwords/czech
CZECH_STOP_WORDS = {
    "a", "aby", "ačkoli", "ahoj", "aj", "ale", "anebo", "ani", "aniž", "ano",
    "asi", "aspoň", "az", "až", "b", "během", "bez", "beze", "blízko",
    "bohužel", "brzo", "bude", "budem", "budeme", "budes", "budeš", "budete",
    "budou", "budu", "by", "byl", "byla", "byli", "bylo", "byly", "bys", "byt",
    "být", "čau", "c", "chce", "chceme", "chceš", "chcete", "chci", "chtějí",
    "chtít", "chut'", "chuti", "ci", "či", "clanek", "článek", "clanku",
    "článku", "clanky", "články", "co", "coz", "což", "čtrnáct", "čtyři", "cz",
    "d", "dál", "dále", "daleko", "dalsi", "další", "děkovat", "děkujeme",
    "děkuji", "den", "deset", "design", "devatenáct", "devět", "dnes", "do",
    "dobrý", "docela", "dva", "dvacet", "dvanáct", "dvě", "e", "email", "f",
    "g", "h", "ho", "hodně", "i", "j", "já", "jak", "jako", "jde", "je",
    "jeden", "jedenáct", "jedna", "jedno", "jednou", "jedou", "jeho", "jej",
    "jeji", "její", "jejich", "jemu", "jen", "jenom", "jenž", "jeste",
    "ještě", "jestli", "jestliže", "ji", "jí", "jich", "jím", "jimi", "jinak",
    "jine", "jiné", "jiz", "již", "jsem", "jses", "jseš", "jsi", "jsme",
    "jsou", "jste", "jšte", "k", "kam", "každý", "kde", "kdo", "kdy", "kdyz",
    "když", "ke", "kolik", "kromě", "ktera", "která", "ktere", "které", "kteri",
    "kteři", "kteří", "kterou", "ktery", "který", "ku", "kvůli", "l", "m",
    "ma", "má", "mají", "málo", "mám", "máme", "máš", "mate", "máte", "me",
    "mé", "mě", "mezi", "mi", "mí", "mit", "mít", "mně", "mnou", "moc", "mohl",
    "mohou", "moje", "moji", "možná", "muj", "můj", "musí", "muze", "může",
    "my", "n", "na", "ná", "nad", "nade", "nam", "nám", "námi", "napiste",
    "napište", "naproti", "nas", "nás", "náš", "naše", "nasi", "naši", "ne",
    "ně", "nebo", "nebyl", "nebyla", "nebyli", "nebyly", "nechť", "něco",
    "nedělá", "nedělají", "nedělám", "neděláme", "neděláš", "neděláte",
    "nějak", "nejsi", "nejsou", "někde", "někdo", "nemají", "nemáme", "nemáte",
    "neměl", "němu", "neni", "není", "nestačí", "nevadí", "nez", "než", "ní",
    "nic", "nich", "ním", "nimi", "nove", "nové", "novy", "nový", "nula",
    "o", "od", "ode", "on", "ona", "oni", "ono", "ony", "osm", "osmnáct",
    "p", "pak", "patnáct", "pět", "po", "pod", "podle", "pokud", "pořád",
    "potom", "pouze", "pozdě", "prave", "práve", "pred", "před", "přede",
    "pres", "přes", "přese", "pri", "při", "pro", "proc", "proč", "prosím",
    "prostě", "proti", "proto", "protoze", "protože", "prvni", "první", "pta",
    "q", "r", "re", "rovně", "s", "se", "sedm", "sedmnáct", "šest", "šestnáct",
    "si", "sice", "skoro", "smějí", "smí", "snad", "spolu", "sta", "sté", "sto",
    "strana", "sve", "své", "svůj", "svych", "svých", "svym", "svým", "svymi",
    "svými", "t", "ta", "tady", "tak", "take", "také", "takhle", "taky",
    "takze", "takže", "tam", "tamhle", "tamhleto", "tamto", "tato", "te", "tě",
    "tebe", "tebou", "ted'", "tedy", "tema", "těma", "ten", "tento", "teto",
    "této", "ti", "tim", "tím", "timto", "tímto", "tipy", "tisíc", "tisíce",
    "to", "tobě", "tohle", "toho", "tohoto", "tom", "tomto", "tomuto", "toto",
    "třeba", "tři", "třináct", "trošku", "tu", "tuto", "tvá", "tvé", "tvoje",
    "tvůj", "ty", "tyto", "u", "určitě", "uz", "už", "v", "vam", "vám", "vámi",
    "vas", "vás", "váš", "vase", "vaše", "vaši", "ve", "večer", "vedle",
    "vice", "více", "vlastně", "vsak", "však", "všechen", "všechno", "všichni",
    "vůbec", "vy", "vždy", "w", "x", "y", "z", "za", "zač", "zatímco", "zda",
    "zde", "ze", "že", "zpet", "zpět", "zpravy", "zprávy"
}


def czech_stop_word_filter(words):
    return [word for word in words if word not in CZECH_STOP_WORDS]


def no_stop_words_filter(words):
    """
    We do not use stop words as for example
    https://www.wikidata.org/wiki/Q24704949 name is  "Pro forma" removing
    "pro" as a stop word would lead to many mappings. Based only on
    "forma" with 100% share.
    """
    return words


INVALID_MAPPING_TOKENS = {"(", ")", ".", "?", "!", "-", ",", "}", "{"}


def invalid_standalone_mapping_terms_filter(words):
    # For example "-" can be used to map to:
    # Q11879093 or Q10689378 .. as only shared terms
    # While we allow "-" to be used as a shared term it must
    # not be the only shared term
    return [
        word for word in words
        if word not in INVALID_MAPPING_TOKENS
    ]  # TODO Add CZECH_STOP_WORDS


def mapping_selector(item: any) -> typing.List[WikidataMappingSelectorResult]:
    def mapping_factory(entity, shared_words, target_words):
        return {
            "id": entity,
            "metadata": {
                "group": shared_words,
                "shared_size": len(shared_words),
                "target_size": len(target_words)
            }
        }

    # Select and delete mapping source.
    source = item["mappings-value"]
    del item["mappings-value"]

    #
    item["mappings"] = item.get("mappings", [])
    target = item["mappings"]
    return [
        WikidataMappingSelectorResult(
            lambda: [source["title"]],
            mapping_factory,
            lambda mappings: target.append({
                "metadata": {
                    "from": "title",
                    "title": "Wikidata",
                    "input": source["title"]
                },
                "data": mappings,
            })
        ),
        WikidataMappingSelectorResult(
            lambda: [source["description"]],
            mapping_factory,
            lambda mappings: target.append({
                "metadata": {
                    "from": "description",
                    "title": "Wikidata",
                    "input": source["description"]
                },
                "data": mappings,
            })
        ),
        WikidataMappingSelectorResult(
            lambda: source["keywords"],
            mapping_factory,
            lambda mappings: target.append({
                "metadata": {
                    "from": "keywords",
                    "title": "Wikidata",
                    "input": source["keywords"]
                },
                "data": mappings,
            })
        )
    ]


def mapping_for_hierarchy_selector(item: any) \
        -> typing.Generator[str, None, None]:
    for mappings in item["mappings"]:
        for mapping in mappings["data"]:
            yield mapping["id"]


def set_hierarchy(entity: any, hierarchy: typing.List):
    entity["hierarchy"] = hierarchy


def get_hierarchy(entity: any) -> typing.List:
    return entity["hierarchy"]


def mapping_selector(item: any) -> typing.List[ReduceMappingSelectorResult]:
    def getter(mapping):
        return mapping["data"]

    def setter(mapping, data):
        mapping["data"] = data

    result = []
    for item in item["mappings"]:
        # As we create the functions in loop we use partial,
        # otherwise it would use the last value of mapping.
        result.append(ReduceMappingSelectorResult(
            functools.partial(getter, item),
            functools.partial(setter, item)))

    return result


def create_mapped_entity(mapping: any, target_id: str) -> any:
    metadata = mapping["metadata"]
    return {
        "id": target_id,
        "metadata": {
            "group": metadata["group"],
            "reduced_from": [mapping["id"]],
            "directly_mapped": False,
        }
    }


def create_originally_mapped(mapping: any):
    """We mark mappings that were """
    metadata = mapping["metadata"]
    return {
        "id": mapping["id"],
        "metadata": {
            "group": metadata["group"],
            "directly_mapped": True,
            "directly_mapped_group": metadata["group"]
        }
    }


def merge_mappings(left: any, right: any, new_id: str) -> any:
    return {
        "id": new_id,
        "metadata": merge_mapping_metadata(left["metadata"], right["metadata"]),
    }


def merge_mapping_metadata(
        left: typing.Dict, right: typing.Dict) -> typing.Dict:
    """Merge mapping's matedata, preserve only some attributes."""
    # Keys: reduced_from, group, shared_size, target_size

    result = {
        "group": list({*left["group"], *right["group"]}),
        "reduced_from": list({
            *left.get("reduced_from", []),
            *right.get("reduced_from", [])
        }),
        "directly_mapped": left["directly_mapped"] or right["directly_mapped"]
    }

    directly_mapped_group = [
        *left.get("directly_mapped_group", []),
        *right.get("directly_mapped_group", [])
    ]
    if directly_mapped_group:
        result["directly_mapped_group"] = directly_mapped_group

    return result


def get_reduced_from(entity: any) -> typing.Generator[str, None, None]:
    for mappings in entity["mappings"]:
        for mapping in mappings["data"]:
            for reduce_from in mapping["metadata"].get("reduced_from", []):
                yield reduce_from


if __name__ == "__main__":
    multiprocessing.current_process().name = "main"
    main()
