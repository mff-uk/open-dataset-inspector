#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import yaml
from flask import Flask, request, jsonify

from compute_graph_similarity import \
    load_dataset_from_json, find_all_path, select_closes_for_each

app = Flask(__name__)

configuration = {}

@app.route("/", methods=["POST"])
def parse_request():
    files = request.files.to_dict(flat=False)
    [left, right] = [
        load_dataset_from_json(json.load(file))
        for file in files["dataset"]
    ]
    all_paths = find_all_path(left, right)
    closest_paths = select_closes_for_each(all_paths)
    return jsonify(closest_paths)


def load_configuration():
    with open(os.path.join("..", "config.yaml")) as file:
        return yaml.load(file, Loader=yaml.FullLoader)["configuration"]


if __name__ == "__main__":
    configuration = load_configuration()
    app.run(port=configuration["pathServicePort"])
