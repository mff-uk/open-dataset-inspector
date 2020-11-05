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
# Requires data as produced by: run_import_datasets.py
#

import os
import json
import csv
import functools


def main():
    # Names of CSV files in ../data/similarities-matrix/ directory that
    # should be imported.
    names = [
        # .
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
        #
        "nkod-title.bert.vector.cosine",
        "nkod-title.udpipe-f.reduce.word2vec[labels.80.40.d].vector.cosine",
        "nkod-title.udpipe-f.reduce.hausdorff[labels.80.40.d]",
        "nkod-description.bert.vector.cosine",
        "nkod-description.udpipe-f.reduce.word2vec[labels.160.40.d].vector.cosine",
        "nkod-description.udpipe-f.reduce.hausdorff[labels.80.40.d]",
        "nkod-wikidata-concepts-d.concat.reduce.word2vec[concepts.80.40.d].vector.cosine",
        "nkod-wikidata-concepts.concat.reduce.word2vec[concepts.40.10.d].vector.cosine"
    ]
    for name in names:
        convert(
            # Translation from IRI to file name.
            "../data/dataset-iri-to-file-name.json",
            # File with pairs "iri", "title" , the important thing is
            # that this defined order of records in the matrix.
            "../data/similarities-matrix/nkod-20-title.csv",
            # The similarity matrix.
            "../data/similarities-matrix/nkod-20/" + name + ".csv",
            # Output path.
            "../data/similarities/" + name + "/"
        )


def convert(
        dataset_to_file_name_file:str,
        header_file:str,
        similarity_file:str,
        target_directory:str
):
    print("Converting", similarity_file, "...")
    iri_to_file_name = load_json(dataset_to_file_name_file)
    iris = read_dataset_iris(header_file)
    os.makedirs(target_directory, exist_ok=True)
    with open(similarity_file) as stream:
        reader = csv.reader(stream, delimiter=",")
        for row_index, [row, iri] in enumerate(zip(reader, iris)):
            rows = [
                [str_to_float(x)]
                for index, x in enumerate(row)
            ]
            # We need to remove 'inf' values. So we replace them with max +1.
            output_path = os.path.join(
                target_directory, iri_to_file_name[iri] + ".csv")
            write_csv(output_path, ["score"], rows)
    output_path = os.path.join(target_directory, "datasets.csv")
    write_csv(output_path, ["iri"], [[iri] for iri in iris])


@functools.lru_cache(maxsize=6)
def load_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def read_dataset_iris(path):
    with open(path, encoding="utf-8") as stream:
        reader = csv.reader(stream, delimiter=",", quotechar='"')
        next(reader)
        return [line[0] for line in reader]


def str_to_float(value: str) -> float:
    return float(value)


def write_csv(file_path, header, rows):
    with open(file_path, "w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(
            stream, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main()
