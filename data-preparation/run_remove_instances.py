#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Takes './www.wikidata.org/' and remove nodes that have only out-coming
# instanceOf edges.
#
# Input: 53.208.214 Output: 1.534.909
#

import json
import itertools
import time


def main():
    start = time.process_time()
    nodes_to_keep = set()

    directory = "../data/www.wikidata.org/"
    output_file_name = "wikidata-hierarchy-reduced.trie.jsonl"

    print("Searching for inner nodes and nodes with subclassOf edge ..")
    counter = 0
    with open(directory + "wikidata-hierarchy.jsonl") as input_stream:
        for line in input_stream:
            content = json.loads(line)
            instance = content.get("instanceof", [])
            subclass = content.get("subclassof", [])
            # Keep all inner nodes.
            for node_id in itertools.chain(instance, subclass):
                nodes_to_keep.add(node_id)
            # Keep those with subclass edge.
            if subclass:
                nodes_to_keep.add(content["id"])
            counter += 1
            if counter % 250000 == 0:
                print("  ", counter)
    total_count = counter
    print(f'Finished in {int(time.process_time() - start)} s')

    print("Creating output ....")
    counter = 0
    with open(directory + "wikidata-hierarchy.jsonl") as input_stream, \
            open(directory + output_file_name, "w") as output_stream:
        for line in input_stream:
            content = json.loads(line)
            if content["id"] not in nodes_to_keep:
                continue
            if "instanceof" in content:
                content["instanceof"] = filter_array(
                    nodes_to_keep, content["instanceof"])
            if "subclassof" in content:
                content["subclassof"] = filter_array(
                    nodes_to_keep, content["subclassof"])
            output_stream.write(json.dumps(content))
            output_stream.write("\n")
            counter += 1
            if counter % 250000 == 0:
                print("  ", counter)

    print(f'Input: {total_count} Output: {len(nodes_to_keep)}')
    print(f'Finished in {int(time.process_time() - start)} s')


def filter_array(items_to_keep, items):
    return [item for item in items if item in items_to_keep]


if __name__ == "__main__":
    main()
