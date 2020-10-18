#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Update values (labels, description, aliases) for wikidata and datasets,
# so they can be later used for mapping.
#
# Requires data as produced by: run_prepare_data_gov_cz.py
# Requires: pip install ufal.udpipe
#

import json
import os
import logging
import typing
import functools
import unidecode

from ufal.udpipe import Model, Sentence, ProcessingError

from glib import input_output


class UdPipe:

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.error = None

    def load(self, model_path: str):
        logger.info("Loading UdPipe model ...")
        self.model = Model.load(model_path)
        if not self.model:
            raise Exception("Cannot load model from file '%s'." % model_path)
        self.tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not self.tokenizer:
            raise Exception("The model does not have a tokenizer")
        self.error = ProcessingError()

    def transform(self, string: str):
        self.tokenizer.setText(string)

        sentences = []
        sentence = Sentence()
        while self.tokenizer.nextSentence(sentence, self.error):
            self.model.tag(sentence, self.model.DEFAULT)
            sentences.append(sentence)
            sentence = Sentence()

        if self.error.occurred():
            raise Exception(self.error.message)

        words = functools.reduce(
            lambda x, y: x + y,
            [[(w.lemma, w.upostag) for w in s.words] for s in sentences],
            [])
        return [word for word in words if word[1] not in ['<root>']]


logger = input_output.init_logger(logging.getLogger(__name__))


def main():
    udpipe = UdPipe()
    udpipe.load("../data/udpipe/czech-pdt-ud-2.3-181115.udpipe")

    prepare_wikidata_labels(
        udpipe,
        "../data/www.wikidata.org/wikidata-cs.jsonl",
        "../data/working/udpipe-wikidata-cs.jsonl",
        "../data/www.wikidata.org/")

    prepare_nkod(
        udpipe,
        "../data/www.data.gov.cz/2020.04.20-www.data.gov.cz.jsonl",
        "../data/www.data.gov.cz/")


def prepare_wikidata_labels(
        udpipe: UdPipe, in_path: str, cache_path: str, out_directory: str):
    logger.info("Preparing Wikidata ...")

    prepare_wikidata_labels_cache(udpipe, in_path, cache_path)

    export_wikidata_labels(
        in_path,
        out_directory + "wikidata-cs.v1.jsonl",
        extract_value_v1)

    export_wikidata_labels(
        cache_path,
        out_directory + "wikidata-cs.v2.jsonl",
        extract_value_v2)

    export_wikidata_labels(
        cache_path,
        out_directory + "wikidata-cs.v3.jsonl",
        extract_value_v3)

    logger.info("Preparing Wikidata ... done")


def prepare_wikidata_labels_cache(
        udpipe: UdPipe, in_path: str, cache_path: str):
    if os.path.exists(cache_path):
        return
    logger.info("Applying UdPipe to wikidata ..")
    with open(in_path, encoding="utf-8") as in_stream:
        with open(cache_path, "w", encoding="utf-8") as out_stream:
            for counter, line in enumerate(in_stream):
                data = json.loads(line)
                if "label" in data:
                    data["label"] = udpipe.transform(data["label"])
                if "aliases" in data:
                    data["aliases"] = [
                        udpipe.transform(value)
                        for value in data["aliases"]
                    ]
                if counter % 100000 == 0:
                    logger.info("    %i", counter)
                json.dump(data, out_stream)
                out_stream.write("\n")


def extract_value_v1(value: str) -> typing.List[str]:
    """Replace special characters with space."""
    special_characters = [
        "-", "_", "(", ")", "[", "]", "{", "}", ".", ",", ";", ":"
    ]
    value = unidecode.unidecode(value).lower().strip().rstrip()
    for to_replace in special_characters:
        value = value.replace(to_replace, " ")
    return value.split()


def extract_value_v2(value: typing.List[str]) -> typing.List[str]:
    """Extract values from UdPipe, keep only words of given types."""
    # https://universaldependencies.org/u/pos/
    allowed = {"NOUN", "PROPN", "ADJ", "ADP", "NUM", "DET", "VERB"}
    return [unidecode.unidecode(lemma)
            for lemma, lemma_type in value if lemma_type in allowed]


def extract_value_v3(value: typing.List[str]) -> typing.List[str]:
    """
    v2 have issues where "zleva doprava" was changed to "doprava" as "zleva"
    is marked to be adverb. For this reason we keep all word types.
    """
    return [unidecode.unidecode(lemma) for lemma, lemma_type in value]


def export_wikidata_labels(cache_path, out_path, value_update_fnc):
    if os.path.exists(out_path):
        logger.info("Skipping existing file")
        return

    logger.info("Exporting file: %s", out_path)

    with open(cache_path, encoding="utf-8") as in_stream:
        with open(out_path, "w", encoding="utf-8") as out_stream:
            for line in in_stream:
                item = json.loads(line)
                if "label" in item:
                    item["label"] = list(value_update_fnc(item["label"]))
                if "aliases" in item:
                    item["aliases"] = [
                        list(value_update_fnc(value))
                        for value in item["aliases"]
                    ]
                json.dump(item, out_stream)
                out_stream.write("\n")

    logger.info("Exporting ... done")


def prepare_nkod(udpipe: UdPipe, in_path: str, out_directory: str):
    logger.info("Loading NKOD ...")

    with open(in_path, encoding="utf-8") as in_stream:
        data = [json.loads(line) for line in in_stream]

    export_nkod(
        data,
        out_directory + "2020.04.20-www.data.gov.cz.v1.jsonl",
        extract_value_v1)

    udpipe_data = apply_udpipe_to_nkod(udpipe, data)

    export_nkod(
        udpipe_data,
        out_directory + "2020.04.20-www.data.gov.cz.v2.jsonl",
        extract_value_v2)

    export_nkod(
        udpipe_data,
        out_directory + "2020.04.20-www.data.gov.cz.v3.jsonl",
        extract_value_v3)

    logger.info("Preparing NKOD ... done")


def apply_udpipe_to_nkod(udpipe: UdPipe, data):
    result = []
    for counter, item in enumerate(data):
        if counter % 1000 == 0:
            logger.info("    %i/%i", counter, len(data))
        result.append({
            "iri": item["iri"],
            "title": udpipe.transform(item["title"]),
            "description": udpipe.transform(item["description"]),
            "keywords": [udpipe.transform(keyword)
                         for keyword in item["keywords"]]
        })
    return result


def export_nkod(data, out_path, value_update_fnc):
    if os.path.exists(out_path):
        logger.info("Skipping existing file: %s", out_path)
        return

    logger.info("Exporting file: %s", out_path)

    with open(out_path, "w", encoding="utf-8") as out_stream:
        for item in data:
            new_item = {
                "iri": item["iri"],
                "title": value_update_fnc(item["title"]),
                "description": value_update_fnc(item["description"]),
                "keywords": [value_update_fnc(value)
                             for value in item["keywords"]]
            }
            json.dump(new_item, out_stream)
            out_stream.write("\n")

    logger.info("Exporting ... done")


if __name__ == "__main__":
    main()
