#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import collections
import typing
import multiprocessing
from dataclasses import dataclass

from glib.input_output import logger

TransformationContextEntry = collections.namedtuple(
    "TransformationContextEntry", ["iri", "name", "path"])


class TransformationContext:

    def __init__(self, directory: str, write_on_exit=True):
        self.index = {}
        self.directory = directory
        self.write_on_exit = write_on_exit

    def __enter__(self):
        os.makedirs(self.directory, exist_ok=True)
        self._load_index()
        return self

    def _load_index(self):
        index_path = os.path.join(self.directory, "index.json")
        if not os.path.exists(index_path):
            logger.info("No index file found '%s'", index_path)
            return {}
        with open(index_path, encoding="utf-8") as in_stream:
            self.index = json.load(in_stream)
        logger.info("Index of size %s loaded from '%s'",
                    len(self.index), index_path)

    def __exit__(self, *args):
        if self.write_on_exit:
            self._write_index()

    def _write_index(self):
        index_path = os.path.join(self.directory, "index.json")
        logger.info("Saving index to '%s'", index_path)
        with open(index_path, "w", encoding="utf-8") as out_stream:
            json.dump(self.index, out_stream)

    def get(self, object_id: str):
        if object_id not in self.index:
            return None
        return os.path.join(self.directory, self.index[object_id])

    def get_or_create(self, object_id: str, new_extension: str = "json"):
        if object_id not in self.index:
            self.index[object_id] = \
                "item_" + \
                str(len(self.index)).zfill(6) + \
                "." + new_extension
        return os.path.join(self.directory, self.index[object_id])

    def put(self, object_id: str, name: str):
        is_new = object_id not in self.index
        self.index[object_id] = name
        return os.path.join(self.directory, self.index[object_id]), is_new

    def iterate(self) \
            -> typing.Generator[TransformationContextEntry, None, None]:
        for iri, name in self.index.items():
            yield TransformationContextEntry(
                iri, name, os.path.join(self.directory, name))

    def merge(self):
        with DirectoryLock(self.directory):
            self.index.update(self._load_index())
            self._write_index()

    def __len__(self):
        return len(self.index)


class DirectoryLock:

    def __init__(self, file_path, wait_time=5):
        self.lock_path = file_path + ".lock"
        self.sleep_time = wait_time

    def __enter__(self):
        while True:
            try:
                os.makedirs(self.lock_path)
                return
            except:
                time.sleep(self.sleep_time)

    def __exit__(self, *args):
        os.removedirs(self.lock_path)


class NamedThreadPool:

    def __init__(self, threads):
        self._threads = threads
        self._pool = None

    def __enter__(self):
        self._pool = multiprocessing.Pool(
            self._threads, initializer=self.pool_thread_initializer)
        return self._pool

    def __exit__(self, *args):
        self._pool.close()
        self._pool.join()

    @staticmethod
    def pool_thread_initializer():
        name = multiprocessing.current_process().name
        name = "worker " + str(name[name.find("-") + 1:]).zfill(2)
        multiprocessing.current_process().name = name


# region Transformation executor

class AbstractTransformation:
    def __call__(self, input_dir: str, output_dir: str):
        raise NotImplemented()


@dataclass
class TransformationTask:
    iri: str
    is_new: bool
    in_path: str
    out_path: str
    name: str


class AbstractPerTaskTransformation(AbstractTransformation):
    def __call__(self, input_dir: str, output_dir: str):
        with TransformationContext(input_dir, False) as input_context:
            with TransformationContext(output_dir) as output_context:
                for iri, name, in_path in input_context.iterate():
                    out_path, is_new = output_context.put(iri, name)
                    task = TransformationTask(
                        iri, is_new, in_path, out_path, name)
                    self.transform(task)

    def transform(self, task: TransformationTask):
        raise NotImplemented()


@dataclass
class TransformationChunk:
    context: any
    tasks: typing.List[TransformationTask]


class AbstractParallelTransformation(AbstractTransformation):
    def __init__(self, chunk_count, thread_count):
        self._chunk_count = chunk_count
        self._thread_count = thread_count

    def __call__(self, input_dir: str, output_dir: str):
        with TransformationContext(input_dir, False) as input_context:
            with TransformationContext(output_dir) as output_context:
                chunks = self._split_tasks(input_context, output_context)
        with NamedThreadPool(self._thread_count) as pool:
            context = self.get_context()
            pool.map(self.get_worker(), [
                TransformationChunk(context, chunk)
                for chunk in chunks
            ])

    def _split_tasks(
            self,
            input_context: TransformationContext,
            output_context: TransformationContext) \
            -> typing.List[typing.List[TransformationTask]]:
        result = [[] for _ in range(self._chunk_count)]
        for index, (iri, name, in_path) in enumerate(input_context.iterate()):
            out_path, is_new = output_context.put(iri, name)
            result[index % len(result)].append(
                TransformationTask(iri, is_new, in_path, out_path, name)
            )
        return result

    def get_worker(self) -> typing.Callable[[TransformationChunk], None]:
        raise NotImplemented()

    def get_context(self):
        raise NotImplemented()


class Pipeline:

    def __init__(self, directory):
        self._root = directory
        self._steps = []

    def apply(self, transformer: AbstractTransformation) -> "Pipeline":
        self._steps.append({
            "transformer": transformer,
        })
        return self

    def directory(self, directory: str) -> "Pipeline":
        self._steps.append({
            "directory": directory,
        })
        return self

    def execute(self):
        start_time = time.time()
        input_directory = None
        output_directory = None
        skip_step = False
        for index, step in enumerate(self._steps):
            logger.info("Executing step %i / %i", index + 1, len(self._steps))
            if "directory" in step:
                input_directory = output_directory
                output_directory = os.path.join(self._root, step["directory"])
                skip_step = os.path.exists(output_directory)
                logger.info("Output directory changed to '%s'",
                            output_directory)
                os.makedirs(output_directory, exist_ok=True)
            elif skip_step:
                logger.info("Step skipped as output directory already exists")
            elif "transformer" in step:
                transformer: AbstractTransformation = step["transformer"]
                logger.info("Running '%s'",
                            type(transformer).__name__)
                transformer(input_directory, output_directory)
            else:
                raise Exception("Unknown step {}".format(index))
        logger.info("All done in: %s", time.time() - start_time)



# endregion
