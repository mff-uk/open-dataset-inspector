#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import multiprocessing


def init_logger(logger=None):
    if logger is None:
        logger = multiprocessing.get_logger()
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(processName)-20s %(module)-16s [%(levelname)-5s] - %(message)s",
        datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    return logger


logger = init_logger()


def write_json(file: str, content: any):
    with open(file, "w", encoding="utf-8") as stream:
        json.dump(content, stream)


def read_json(file: str):
    with open(file, encoding="utf-8") as stream:
        return json.load(stream)

