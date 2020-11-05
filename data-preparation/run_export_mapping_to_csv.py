#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Export mapping created by `run_mapping_workflow.py` into CSV files, so
# they can be consume by other tools. This was originally designed to export
# mapping for David.
#
# We export only final reduced mapping.
#

import os
import csv
import logging

from glib import input_output

logger = input_output.init_logger(logging.getLogger(__name__))


def main():
    input_output.init_logger()
    export_mapping("../data/mapping/v1", "../data/mapping/v1.csv")


def export_mapping(input_directory: str, output_file: str):
    logger.info("Exporting ... ")
    with open(output_file, "w", newline="") as output_stream:
        writer = csv.writer(output_stream, delimiter=",", quoting=csv.QUOTE_ALL)
        writer.writerow(["dataset", "wikidata entity", "directly mapped"])
        files = os.listdir(input_directory)
        for index, file_name in enumerate(files):
            file_path = os.path.join(input_directory, file_name)
            content = input_output.read_json(file_path)
            writer.writerows([
                [
                    content["@id"],
                    mapping["id"],
                    1 if mapping["metadata"]["directly_mapped"] else 0,
                ]
                for mapping_group in content["mappings"]
                for mapping in mapping_group["data"]
            ])
            if index % 100 == 0:
                logger.info(f"  {index}/{len(files)}")
    logger.info("Exporting ...  done")


if __name__ == "__main__":
    main()
