#!/usr/bin/env python
#
# Import explanation for transitive similarity.
#

import argparse
import os
import json
import csv


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True,
                        help="Path to file with datasets.")
    parser.add_argument("--name", required=True,
                        help="Name of the method")
    parser.add_argument("--odin", required=True,
                        help="Path to ODIN data directory.")
    return vars(parser.parse_args())


def main(arguments):
    directory = os.path.join(
        arguments["odin"], "explanation", arguments["name"])
    os.makedirs(directory, exist_ok=True)
    print("Loading ODIN dataset metadata ...")
    metadata = load_metadata(arguments["odin"])
    print("Loading explanation ...")
    explanation = load_explanation(arguments["input"])
    print("Adding datasets to ODIN metadata ...")
    add_to_mapping(explanation, metadata["mapping"])
    print("Writing ODIN dataset metadata ...")
    write_metadata(arguments["odin"], metadata)
    print("Importing explanations ...")
    import_explanations(directory, explanation, metadata["mapping"])


def load_metadata(directory):
    file = os.path.join(directory, "dataset-metadata.json")
    if not os.path.exists(file):
        return {"mapping": {}}
    with open(file, encoding="utf-8") as stream:
        return json.load(stream)


def load_explanation(file):
    with open(file, encoding="utf-8") as stream:
        return json.load(stream)


def add_to_mapping(explanation, mapping):
    # Collect datasets.
    iris = set()
    for item in explanation:
        iris.add(item["query"])
        iris.add(item["expected"])
        for middle in item["middle"]:
            iris.add(middle)
    # Add all.
    for iri in iris:
        if iri in mapping:
            continue
        output_name = str(len(mapping)).zfill(6)
        mapping[iri] = output_name
    pass


def write_metadata(directory, content):
    file = os.path.join(directory, "dataset-metadata.json")
    with open(file, "w", encoding="utf-8", newline="\n") as stream:
        return json.dump(content, stream, ensure_ascii=False)


def import_explanations(directory, explanation, mapping):
    for item in explanation:
        left, right = sorted([item["query"], item["expected"]])
        file = os.path.join(
            directory,
            mapping[left] + "-" + mapping[right] + ".json")
        content = {
            "datasets": [left, right],
            "explanation": [{
                "dist": item["dist"],
                "lowerBound": item["lower_bound"],
                "upperBound": item["upper_bound"],
                "middle": item["middle"]
            }]
        }
        with open(file, "w", encoding="utf-8", newline="\n") as stream:
            return json.dump(content, stream, ensure_ascii=False)


if __name__ == "__main__":
    main(_parse_arguments())
