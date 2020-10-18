#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import yaml
from flask import Flask, request, jsonify

from compute_graph_similarity import *

app = Flask(__name__)

configuration = {}

path_filter_selectors = {
    "closest": select_closest_for_each,
    "distance": select_paths_by_length
}


@app.route("/", methods=["POST"])
def parse_request():
    files = request.files.to_dict(flat=False)
    [left, right] = [
        load_dataset_from_json(json.load(file))
        for file in files["dataset"]
    ]
    options = json.load(files["options"][0])
    return jsonify(compute_similarity(left, right, options))


def compute_similarity(left, right, options):
    all_paths = find_all_path(left, right)
    method = options.get("method", "closest")
    selected_paths = path_filter_selectors[method](all_paths, options)
    return paths_to_output(selected_paths, [left, right], {
        "method": method,
        "totalPathCount": len(all_paths),
        "resultPathCount": len(selected_paths)
    })


def load_configuration():
    with open(os.path.join("..", "config.yaml")) as file:
        return yaml.load(file, Loader=yaml.FullLoader)["configuration"]


if __name__ == "__main__":
    configuration = load_configuration()
    app.run(port=configuration["pathServicePort"])
