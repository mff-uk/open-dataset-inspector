#!/usr/bin/env python
# 
# Import datasets from metadata records produced by simpipes-components.
#

import argparse
import os
import json


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True,
                        help="Path to directory with dataset files.")
    parser.add_argument("--odin", required=True,
                        help="Path to ODIN data directory.")
    parser.add_argument("--filter", required=False,
                        help="Path to file with dataset.")
    return vars(parser.parse_args())


def main(arguments):
    dataset_filter = create_dataset_filter(arguments["filter"])
    metadata = load_metadata(arguments["odin"])
    import_datasets(
        arguments["input"], arguments["odin"],
        metadata["mapping"], dataset_filter)
    write_metadata(arguments["odin"], metadata)


def create_dataset_filter(filter_file: str):
    def apply_true(iri: str):
        return True

    if filter_file is None:
        return apply_true

    iris = load_text_lines(filter_file)

    def apply_filter(iri: str):
        return iri in iris

    return apply_filter


def load_text_lines(file):
    with open(file, encoding="utf-8") as stream:
        next(stream)
        return {line.rstrip() for line in stream}


def load_metadata(directory):
    file = os.path.join(directory, "dataset-metadata.json")
    if not os.path.exists(file):
        return {"mapping": {}}
    with open(file, encoding="utf-8") as stream:
        return json.load(stream)


def import_datasets(
        input_directory: str, dataset_directory: str,
        mapping: dict[str, str], dataset_filter):
    # Secure output directory.
    os.makedirs(os.path.join(dataset_directory, "dataset"), exist_ok=True)
    #
    file_names = os.listdir(input_directory)
    for file_name in file_names:
        input_path = os.path.join(input_directory, file_name)
        # Load the input file.
        with open(input_path, encoding="utf-8") as stream:
            content = json.load(stream)
        # Apply filters.
        if not dataset_filter(content["iri"]):
            print(file_name, "SKIP", content["iri"])
            continue
        # Get file name.
        print(file_name, " OK ", content["iri"])
        if content["iri"] in mapping:
            output_name = mapping[content["iri"]] + ".json"
        else:
            output_name = str(len(mapping)).zfill(6)
            mapping[content["iri"]] = output_name
        # Convert the content.
        content = convert_dataset_file(content)
        # Write the output.
        output_path = os.path.join(dataset_directory, "dataset", output_name)
        with open(output_path, "w", encoding="utf-8") as stream:
            json.dump(content, stream, ensure_ascii=False)


def convert_dataset_file(content):
    def extract_property(name):
        return content[name].get("data", []) if name in content else ""

    result = {
        "iri": content["iri"],
        "title": {},
        "description": {},
        "keywords": {},
    }

    for language in ["cs", "en"]:
        if "title-" + language in content:
            result["title"][language] = \
                " ".join(extract_property("title-" + language))
        if "description-" + language in content:
            result["description"][language] = \
                " ".join(extract_property("description-" + language))
        if "keywords-" + language in content:
            result["keywords"][language] = \
                extract_property("keywords-" + language)

    return result


def write_metadata(directory, content):
    file = os.path.join(directory, "dataset-metadata.json")
    with open(file, "w", encoding="utf-8") as stream:
        return json.dump(content, stream, ensure_ascii=False)


if __name__ == "__main__":
    main(_parse_arguments())
