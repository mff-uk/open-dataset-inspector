#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Transform TRIG file into JSON-LINES, ignore datasets from CUZK.
#

import rdflib
import collections
import json
import os
import csv

VOCABULARY = {
    "type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
    "Dataset": "http://www.w3.org/ns/dcat#Dataset",
    "keyword": "http://www.w3.org/ns/dcat#keyword",
    "publisher": "http://purl.org/dc/terms/publisher",
    "title": "http://purl.org/dc/terms/title",
    "description": "http://purl.org/dc/terms/description"
}


def main():
    input_file_name = "2020.04.20-www.data.gov.cz"
    source_file = "../data/input/" + input_file_name + ".trig"
    json_lines_file = "../data/www.data.gov.cz/" + input_file_name + ".jsonl"
    print("Preparing json-lines files ...")
    prepare_json_lines(source_file, json_lines_file)
    print("Preparing CSV files ...")
    prepare_csv_files_for_david(
        json_lines_file, "../data/www.data.gov.cz/" + input_file_name)


def prepare_json_lines(source_file, target_file):
    if os.path.exists(target_file):
        print("Output JSON lines file already exists.")
        return
    with open(target_file, "w", encoding="utf-8") as output_stream:
        for rdf_as_str in for_each_graph(source_file):
            graph = rdflib.Graph()
            graph.parse(data=rdf_as_str, format="trig")
            dataset = rdf_graph_to_dataset(graph)
            if dataset is None:
                continue
            json.dump(dataset, output_stream)
            output_stream.write("\n")


def for_each_graph(file):
    with open(file, "r", encoding="utf-8") as input_stream:
        buffer = ""
        for line in input_stream:
            strip_line = line.rstrip()
            if strip_line.startswith("<") and strip_line.endswith("> {"):
                buffer = ""
            elif strip_line == "}":
                yield buffer
                buffer = ""
            else:
                buffer += line


def rdf_graph_to_dataset(graph):
    for iri, entity in rdf_to_entities(graph).items():
        types = [str(x) for x in entity[VOCABULARY["type"]]]
        if VOCABULARY["Dataset"] not in types:
            continue
        publisher = str(entity[VOCABULARY["publisher"]][0])
        # Ignore 'Český úřad zeměměřický a katastrální'
        if publisher == "https://data.gov.cz/zdroj/ovm/00025712":
            return None
        title = str(entity[VOCABULARY["title"]][0])
        description = str(entity[VOCABULARY["description"]][0])
        keywords = [str(keyword) for keyword in entity[VOCABULARY["keyword"]]]
        return {
            "iri": str(iri),
            "title": title,
            "description": description,
            "keywords": keywords,
        }


def rdf_to_entities(graph):
    result = {}
    for s, p, o in graph:
        if s not in result:
            result[s] = collections.defaultdict(list)
        result[s][str(p)].append(o)
    return result


def prepare_csv_files_for_david(source_file, output_prefix):
    with open(source_file, encoding="utf-8") as input_stream:
        datasets = [json.loads(line) for line in input_stream]
    # Write title CSV.
    title_file = output_prefix + ".title.csv"
    write_csv(
        title_file,
        [[dataset["iri"], dataset["title"]] for dataset in datasets],
        ["iri", "title"]
    )
    # Write description CSV.
    description_file = output_prefix + ".description.csv"
    write_csv(
        description_file,
        [[dataset["iri"], dataset["description"]] for dataset in datasets],
        ["iri", "description"]
    )
    # Write keywords CSV.
    keywords_file = output_prefix + ".keywords.csv"
    write_csv(
        keywords_file,
        [[dataset["iri"], keyword]
         for dataset in datasets if len(dataset["keywords"]) > 0
         for keyword in dataset["keywords"]],
        ["iri", "keyword"]
    )


def write_csv(file, rows, header):
    print("Writing CSV with", str(len(rows)).zfill(6), "lines into", file)
    with open(file, "w", encoding="utf-8", newline="") as output_stream:
        writer = csv.writer(
            output_stream,
            delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main()
