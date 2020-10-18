#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# David produce similarity matrices, without dataset's IRIs.
# This script takes those matrices, list of datasets titles and
# mapping from iri to name and prepare data for
# dataset-similarity-visualisation (DSV)
#
# The dataset title file is used to get IRIs for datasets in the similarity
# matrix as the order is the same.
#
# The same IRI to file mapping must be used to prepare all data for
# DSV. The reason is that DSV need one file per dataset and as IRI can't
# be easily converted to nice file name we use translation table,
# i.e. IRI to file mapping.
#
# See main function to get paths to all relevant files.
#
# We replace +inf with biggest number smaller then infinity + 1.
# This is needed as 'inf' is not a valid number in CSV.
#
# Requires data as produced by: run_prepare_data_gov_cz.py
#

import os
import json
import csv
import functools

def main():
    json_lines_file = "../data/www.data.gov.cz/2020.04.20-www.data.gov.cz.jsonl"
    prepare_datasets_for_ui(json_lines_file, "../data/datasets")

    names = [
        "nkod-_title_description_.join.reduce.tlsh.tlsh",
        "nkod-description.udpipe-f.reduce.hausdorff[cswiki]",
        "nkod-description.udpipe-f.reduce.hausdorff[law]",
        "nkod-description.udpipe-f.reduce.word2vec[cswiki].vector.cosine",
        "nkod-description.udpipe-f.reduce.word2vec[law].vector.cosine",
        "nkod-description.udpipe-f.reduce.words_count.cosine",
        "nkod-keywords.concat.reduce.set.jaccard",
        "nkod-title.udpipe-f.reduce.hausdorff[cswiki]",
        "nkod-title.udpipe-f.reduce.hausdorff[law]",
        "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine",
        "nkod-title.udpipe-f.reduce.word2vec[law].vector.cosine",
        "nkod-title.udpipe-f.reduce.words_set.jaccard",
    ]
    for name in names:
        convert(
            "../data/dataset-iri-to-file-name.json",
            "../lindas/data/sources/nkod-20/nkod-title.csv",
            "../lindas/data/matrix/nkod-20/" + name + ".csv",
            "../data/web-data/similarities/" + name + "/"
        )


def convert(
        dataset_to_file_name_file, header_file,
        similarity_file, target_directory):
    print("Converting", similarity_file, "...")
    iri_to_file_name = load_json(dataset_to_file_name_file)
    iris = read_dataset_iris(header_file)
    os.makedirs(target_directory, exist_ok=True)
    with open(similarity_file) as stream:
        reader = csv.reader(stream, delimiter=",")
        for row_index, [row, iri] in enumerate(zip(reader, iris)):
            rows = [
                [strToFloat(x)]
                for index, x in enumerate(row)
            ]
            # We need to remove 'inf' values. So we replace them with max +1.
            output_path = os.path.join(
                target_directory, iri_to_file_name[iri] + ".csv")
            write_csv(output_path, ["score"], rows)
    output_path = os.path.join(target_directory, "datasets.csv")
    write_csv(output_path, ["iri"], [[iri] for iri in iris])


@functools.lru_cache
def load_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def read_dataset_iris(path):
    with open(path, encoding="utf-8") as stream:
        reader = csv.reader(stream, delimiter=",", quotechar='"')
        next(reader)
        return [line[0] for line in reader]


def strToFloat(value: str) -> float:
    return float(value)


def write_csv(file_path, header, rows):
    with open(file_path, "w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(
            stream, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def prepare_datasets_for_ui(source_file, output_directory):
    print("Writing dataset detail files ..")
    os.makedirs(output_directory, exist_ok=True)
    with open(source_file, encoding="utf-8") as input_stream:
        datasets = [json.loads(line) for line in input_stream]
    index_content = {}
    for dataset in datasets:
        file_name = (str(len(index_content))).zfill(6)
        output_file = os.path.join(output_directory, file_name + ".json")
        with open(output_file, "w", encoding="utf-8") as output_stream:
            json.dump(dataset, output_stream)
        index_content[dataset["iri"]] = file_name
    index_file = os.path.join(
        output_directory, "..", "dataset-iri-to-file-name.json"
    )
    with open(index_file, "w", encoding="utf-8") as output_stream:
        json.dump(index_content, output_stream)


if __name__ == "__main__":
    main()
