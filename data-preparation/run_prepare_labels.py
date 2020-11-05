# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Collect all entities in mapped hierarchy and extract labels for them.
# The extracted labels are used in frontend.
#

import os
import json


def main():
    dataset_directory = "../data/mapping/v1"
    input_labels_file = "../data/www.wikidata.org/wikidata-en.jsonl"
    output_file = "../data/www.wikidata.org/wikidata-labels-en.jsonl"
    entities = collect_entities(dataset_directory)
    filter_file(input_labels_file, entities, output_file)


def collect_entities(directory: str):
    result = set()
    print("Loading dataset files ...")
    for index, file in enumerate(os.listdir(directory)):
        if index > 0 and index % 1000 == 0:
            print("   ", index)
        path = os.path.join(directory, file)
        content = load_json(path)
        for item in content["hierarchy"]:
            result.add(item[0])
            result.add(item[1])
        for mapping in content["mappings"]:
            for item in mapping["data"]:
                result.add(item["id"])
    print("Loading dataset files ... done")
    return result


def load_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def filter_file(input_file: str, entries, output_file: str):
    print("Filtering labels ...")
    with open(input_file, encoding="utf-8") as in_stream:
        with open(output_file, "w", encoding="utf-8") as out_stream:
            for index, line in enumerate(in_stream):
                if index > 0 and index % 100000 == 0:
                    print("   ", index)
                content = json.loads(line)
                if content["id"] not in entries:
                    continue
                if "label" not in content:
                    print("    missing for used entity label:", content)
                    continue
                out_stream.write(json.dumps({
                    "id": content["id"],
                    "label": content["label"],
                }))
                out_stream.write("\n")
    print("Filtering labels ... done")

if __name__ == "__main__":
    main()
