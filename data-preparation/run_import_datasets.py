#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Prepare datasets into ../data/datasets that are used by the UI. For each
# dataset we store metadata like iri, title, description and keywords.
# It also produce file called dataset-iri-to-file-name.json that maps
# data set IRI to a file name. We do this as IRI can not be used as a file name.
#
# Requires data as produced by: run_prepare_data_gov_cz.py
#


import os
import json
import csv
import functools


def main():
    # Input file with all datasets.
    json_lines_file = "../data/www.data.gov.cz/2020.04.20-www.data.gov.cz.jsonl"
    prepare_datasets_for_ui(json_lines_file, "../data/datasets")


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
