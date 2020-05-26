#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import collections
import numpy
import typing
from dataclasses import dataclass


@dataclass
class RawEvaluation:
    user: str
    group: str
    useCase: str
    rating: typing.Dict[str, float]


@dataclass
class Score:
    value: float
    useCase: str


@dataclass
class MethodEvaluation:
    method: str
    scores: typing.List[Score]


class EvaluationStatistics:
    method: str
    scores: typing.List[Score]
    min: float
    max: float
    mean: float
    median: float

    def __init__(self, method: str, scores: typing.List[Score]):
        self.method = method
        self.scores = scores
        score_values = [item.value for item in scores]
        self.min = min(score_values)
        self.max = max(score_values)
        self.mean = numpy.mean(score_values)
        self.median = numpy.median(score_values)


def main():
    evaluations = load_evaluations()
    evaluations = [item for item in evaluations
                   if item.user not in ["Test", "MaNe"]]

    evaluations = normalize_with_respect_to_method(
        evaluations, "nkod-_title_description_.join.reduce.tlsh.tlsh")

    print("# all data count:", len(evaluations))
    evaluate_and_print(evaluations)
    for user, user_evaluations in iterate_per_user(evaluations):
        print()
        print("# user:", user, "count:", len(user_evaluations))
        evaluate_and_print(user_evaluations)


def load_evaluations() -> typing.List[RawEvaluation]:
    evaluation_directory = "../data/evaluation-reports"
    result = []
    for file_name in os.listdir(evaluation_directory):
        file_path = os.path.join(evaluation_directory, file_name)
        with open(file_path, encoding="utf-8") as stream:
            content = json.load(stream)
        if content["task"]["action"] != "submit":
            continue
        result.append(RawEvaluation(
            content["task"]["user"],
            content["task"]["group"],
            content["task"].get("useCaseId", None),
            {key: float(value) for key, value in content["rating"].items()}
        ))
    return result


def normalize_with_respect_to_method(
        data: typing.List[RawEvaluation], method: str) \
        -> typing.List[RawEvaluation]:
    """
    We collect data as user ratings, but user may rate all methods with same
    number 0 or 5 - we need to consider both of these the same.

    For this reason we normalize the values into interval <-1, 1> when 0
    is equal score of the method of given name. Thus the given method is
    used as a baseline.

    In the input we also assume that smaller is better as the input is
    ordering. Here 1 is best and -1 is worst compared to the given method.
    """
    result = []
    for item in data:
        baseline = item.rating[method]
        min_value = min(item.rating.values()) - baseline
        max_value = max(item.rating.values()) - baseline
        scale = max(abs(max_value), abs(min_value))

        def normalize(value: float) -> float:
            """
            Center by subtracting given method result scale to -1, 1 by where
            either -1 or 1 is the min. or max valuerespectively.
            We can not scale to full -1, 1 always as we need the ref
            method to be zero.
            """
            if scale == 0:
                return 0
            result = - (value - baseline) / scale
            # Python use negative zero, by next condition we get rid of it.
            return 0 if result == 0 else result

        rating = {
            key: normalize(value)
            for key, value in item.rating.items()
        }
        result.append(RawEvaluation(
            item.user, item.group, item.useCase, rating))
    return result


def evaluate_and_print(evaluations: typing.List[RawEvaluation]):
    ratings = collect_methods_ratings(evaluations)
    statistics = [EvaluationStatistics(item.method, item.scores)
                  for item in ratings]
    print_statistics(statistics)


def collect_methods_ratings(
        data: typing.List[RawEvaluation]) -> typing.List[MethodEvaluation]:
    result = collections.defaultdict(list)
    for user_evaluation in data:
        for method, method_rating in user_evaluation.rating.items():
            result[method].append(Score(
                method_rating, user_evaluation.useCase))
    return [MethodEvaluation(method, values)
            for method, values in result.items()]


def print_statistics(
        statistics: typing.List[EvaluationStatistics],
        ref_method="nkod-_title_description_.join.reduce.tlsh.tlsh",
        print_values=True):
    use_cases = sorted({
        score.useCase
        for stats in statistics
        for score in stats.scores})

    print("# use-cases:", "'" + "', '".join(use_cases) + "'")

    sorted_stats = sorted(statistics, key=lambda x: x.mean, reverse=True)
    for item in sorted_stats:
        print("{:<70} median: {: 03.2f} min: {: 03.2f} max: {: 03.2f}".format(
            item.method, item.median, item.min, item.max), end="")
        if item.method == ref_method:
            print(" [REF] ", end="")
        else:
            print("       ", end="")
        if print_values:
            scores_dict = {score.useCase: score.value for score in item.scores}
            values = [
                scores_dict.get(use_case, None)
                for use_case in scores_dict
            ]
            print(", ".join(["{: 03.2f}".format(x) for x in values]))


def iterate_per_user(evaluations: typing.List[RawEvaluation]):
    users = {item.user for item in evaluations}
    for user in users:
        yield user, [item for item in evaluations if item.user == user]


if __name__ == "__main__":
    main()
