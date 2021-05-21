#!/usr/bin/env python
#
# Import similarity matrix.
#

import argparse
import os
import json
import csv


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", required=True,
                        help="Path to CSV file with dataset IRIs.")
    parser.add_argument("--matrix", required=True,
                        help="Path to similarity matrix.")
    parser.add_argument("--name", required=True,
                        help="Name of the method")
    parser.add_argument("--odin", required=True,
                        help="Path to ODIN data directory.")
    return vars(parser.parse_args())


def main(arguments):
    directory = os.path.join(
        arguments["odin"], "similarity", arguments["name"])
    os.makedirs(directory, exist_ok=True)
    print("Loading ODIN dataset metadata ...")
    metadata = load_metadata(arguments["odin"])
    print("Loading dataset IRIs ...")
    iris = load_dataset_iri(arguments["datasets"])
    print("Adding datasets to ODIN metadata ...")
    add_to_mapping(iris, metadata["mapping"])
    print("Writing ODIN dataset metadata ...")
    write_metadata(arguments["odin"], metadata)
    print("Writing datasets file ...")
    write_dataset_file(os.path.join(directory, "datasets.csv"), iris)
    print("Processing similarity matrix ...")
    import_matrix(
        directory,
        metadata["mappping"],
        iris,
        arguments["matrix"])
    print(
        "Please create a metadata entry in '"
        + os.path.join(arguments["odin"], "similarity-metadata.json")
        + "' for" + arguments["name"])


def load_metadata(directory):
    file = os.path.join(directory, "dataset-metadata.json")
    if not os.path.exists(file):
        return {"mapping": {}}
    with open(file, encoding="utf-8") as stream:
        return json.load(stream)


def load_dataset_iri(path):
    """Load first CSV column as dataset IRIs."""
    with open(path) as stream:
        reader = csv.reader(stream, delimiter=",")
        next(reader)
        return [row[0] for row in reader]


def add_to_mapping(iris, mapping):
    for iri in iris:
        if iri in mapping:
            continue
        output_name = str(len(mapping)).zfill(6)
        mapping[iri] = output_name
    pass


def write_dataset_file(file, iris):
    with open(file, "w", encoding="utf-8", newline="\n") as stream:
        stream.write("iri")
        for iri in iris:
            stream.write(iri)


def import_matrix(directory, mapping, iris, matrix):
    """

    :param directory: Path to output directory.
    :param mapping: Mapping from IRI to file name.
    :param iris: Dataset IRIs.
    :param matrix: Path to the matrix.
    :return:
    """
    with open(matrix) as stream:
        reader = csv.reader(stream, delimiter=",")
        for row, iri in zip(reader, iris):
            file = os.path.join(directory, mapping[iri] + ".csv")
            write_similarity_file(file, row)


def write_similarity_file(file, values):
    with open(file, "w", encoding="utf-8", newline="\n") as stream:
        stream.write("score")
        for value in values:
            stream.write(value)


def write_metadata(directory, content):
    file = os.path.join(directory, "dataset-metadata.json")
    with open(file, "w", encoding="utf-8", newline="\n") as stream:
        return json.dump(content, stream, ensure_ascii=False)


if __name__ == "__main__":
    main(_parse_arguments())
