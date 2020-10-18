#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Produce evaluation-reports-summary.json file .
#

import os
import json
import collections
import numpy
import typing
import datetime
import dateutil.parser
import copy
from dataclasses import dataclass


@dataclass
class RawEvaluation:
    session: str
    user: str
    group: str
    use_case: str
    rating: typing.Dict[str, float]
    raw_rating: typing.Dict[str, float]
    load_time: datetime.datetime
    submit_time: datetime.datetime


@dataclass
class RawEvaluationAction(RawEvaluation):
    """Action type causing the """
    action: str


@dataclass
class RawEvaluationSubmit(RawEvaluation):
    """Times of evaluation actions without submit."""
    action_times: typing.List[datetime.datetime]


@dataclass
class Score:
    value: float
    evaluation: RawEvaluationSubmit


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
    evaluate_iiwas_2020()


def evaluate_iiwas_2020():
    evaluation_directory = "../data/evaluation-reports-archive/20200621"
    evaluations = load_evaluations(evaluation_directory)
    evaluations = [item for item in evaluations
                   if item.user not in ["Test", "MaNe"]]
    evaluations = normalize_with_respect_to_method(
        evaluations, "nkod-_title_description_.join.reduce.tlsh.tlsh")
    evaluations = keep_last_submits(evaluations)

    export_evaluations(
        evaluations,
        "../data/evaluation-reports-archive/"
        "20200621-evaluation-reports-summary.json"
    )

    evaluate_and_print(evaluations)

    for user, user_evaluations in iterate_per_user(evaluations):
        print("# user:", user, "count:", len(user_evaluations))
        evaluate_and_print(user_evaluations)


def load_evaluations(
        evaluation_directory: str) -> typing.List[RawEvaluationSubmit]:
    result = []
    for file_name in os.listdir(evaluation_directory):
        file_path = os.path.join(evaluation_directory, file_name)
        with open(file_path, encoding="utf-8") as stream:
            content = json.load(stream)
        result.append(RawEvaluationAction(
            content["task"]["session"],
            content["task"]["user"],
            content["task"]["group"],
            content["task"].get("useCaseId", None),
            {},
            {key: float(value) for key, value in content["rating"].items()},
            dateutil.parser.parse(content["task"]["timeLoad"]),
            dateutil.parser.parse(content["task"]["timePost"]),
            content["task"]["action"]
        ))
    return group_raw_results(result)


def group_raw_results(evaluations: typing.List[RawEvaluationAction]) \
        -> typing.List[RawEvaluationSubmit]:
    considered_actions = ["change-method-order", "change-method-order-number"]
    collector = collections.defaultdict(list)
    for item in evaluations:
        identification = item.session + item.user + str(item.load_time)
        collector[identification].append(item)
    result = []
    for items in collector.values():
        action_times = sorted([
            item.submit_time for item in items
            if item.action in considered_actions
        ])
        submit = [item for item in items if item.action == "submit"]
        if not len(submit) == 1:
            continue
        submit_item: RawEvaluation = submit[0]
        result.append(RawEvaluationSubmit(
            submit_item.session,
            submit_item.user,
            submit_item.group,
            submit_item.use_case,
            submit_item.rating,
            submit_item.raw_rating,
            submit_item.load_time,
            submit_item.submit_time,
            action_times
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
        baseline = item.raw_rating[method]
        scale = max([
            abs(value - baseline)
            for value in item.raw_rating.values()
        ])

        def normalize(value: float) -> float:
            """
            Center by subtracting given method result scale to -1, 1 by where
            either -1 or 1 is the min. or max valuerespectively.
            We can not scale to full -1, 1 always as we need the ref
            method to be zero.
            """
            if scale == 0:
                return 0
            normalized_value = - (value - baseline) / scale
            # Python use negative zero, by next condition we get rid of it.
            return 0 if normalized_value == 0 else normalized_value

        rating = {
            key: normalize(value)
            for key, value in item.raw_rating.items()
        }
        result_item = copy.copy(item)
        result_item.rating = rating
        result.append(result_item)
    return result


def keep_last_submits(data: typing.List[RawEvaluation]) \
        -> typing.List[RawEvaluation]:
    result = {}
    for item in data:
        ref = item.user + ":" + item.use_case
        if ref not in result:
            result[ref] = item
        elif result[ref].submit_time < item.submit_time:
            result[ref] = item
    return list(result.values())


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
                method_rating, user_evaluation))
    return [MethodEvaluation(method, values)
            for method, values in result.items()]


def print_statistics(
        statistics: typing.List[EvaluationStatistics],
        ref_method="nkod-_title_description_.join.reduce.tlsh.tlsh",
        print_values=True,
        print_durations=True):
    use_cases = sorted({
        score.evaluation.use_case
        for stats in statistics
        for score in stats.scores},
        key=lambda value: int(value)
    )

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
            scores_by_use_case = {
                score.evaluation.use_case: score.value
                for score in item.scores
            }
            values = [scores_by_use_case.get(use_case, None)
                      for use_case in use_cases]
            print(", ".join(["{: 03.2f}".format(x) for x in values]))

    if print_durations:
        scores_by_use_case = collections.defaultdict(list)
        for score in sorted_stats[0].scores:
            scores_by_use_case[score.evaluation.use_case].append(score)
        import pprint
        duration_by_use_case = {
            use_case: numpy.mean(get_scores_evaluation_durations(scores))
            for use_case, scores in scores_by_use_case.items()
        }
        values = [duration_by_use_case.get(use_case, None)
                  for use_case in use_cases]
        print(" " * 113, end="")
        print(", ".join(["{:5d}".format(int(x)) for x in values]))


def get_scores_evaluation_durations(scores: typing.List[Score]) \
        -> typing.List[float]:
    scores_durations = []
    for score in scores:
        start = score.evaluation.action_times[0]
        duration = (score.evaluation.submit_time - start).total_seconds()
        scores_durations.append(duration)
    return scores_durations


def iterate_per_user(evaluations: typing.List[RawEvaluation]):
    users = {item.user for item in evaluations}
    for user in users:
        yield user, [item for item in evaluations if item.user == user]


def export_evaluations(
        evaluations: typing.List[RawEvaluationSubmit], output: str):
    result = []
    date_format = "%Y.%m.%dT%H:%M:%S"
    for evaluation in evaluations:
        result.append({
            "user": evaluation.user,
            "use-case": evaluation.use_case,
            "load-time": evaluation.load_time.strftime(date_format),
            "submit-time": evaluation.submit_time.strftime(date_format),
            "action-time": [time.strftime(date_format)
                            for time in evaluation.action_times],
            "rating": evaluation.rating,
            "raw-rating": evaluation.raw_rating,
        })
    with open(output, "w", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)


if __name__ == "__main__":
    main()
