#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import os
from pprint import pprint

import numpy

import plotly
import plotly.express

# Plotly use Orca to create static images.
plotly.io.orca.config.executable = \
    "C:/Users/Petr/AppData/Local/Programs/orca/orca.exe"

OUTPUT_ROOT = "../data/evaluation-reports-graphs/"

METHOD_LABELS = {
    "nkod-_title_description_.join.reduce.tlsh.tlsh": "tlsh : title description",
    "nkod-description.udpipe-f.reduce.hausdorff[cswiki]": "hausdorff : description [cswiki]",
    "nkod-description.udpipe-f.reduce.hausdorff[law]": "hausdorff : description [law]",
    "nkod-description.udpipe-f.reduce.word2vec[cswiki].vector.cosine": "cosine : description [cswiki]",
    "nkod-description.udpipe-f.reduce.word2vec[law].vector.cosine": "cosine : description [law]",
    "nkod-description.udpipe-f.reduce.words_count.cosine": "cosine : description",
    "nkod-keywords.concat.reduce.set.jaccard": "jaccard : keywords",
    "nkod-title.udpipe-f.reduce.hausdorff[cswiki]": "hausdorff : title [cswiki]",
    "nkod-title.udpipe-f.reduce.hausdorff[law]": "hausdorff : title [law]",
    "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine": "cosine : title [cswiki]",
    "nkod-title.udpipe-f.reduce.word2vec[law].vector.cosine": "cosine : title [law]",
    "nkod-title.udpipe-f.reduce.words_set.jaccard": "jaccard : title"
}


def main():
    evaluations = load_json("../data/evaluation-reports-summary.json")
    pprint(evaluations[0])
    print("-" * 80)
    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    prepare_index()
    plot_data(evaluations)
    finalize_index()


def prepare_index():
    with open(os.path.join(OUTPUT_ROOT, "index.html"), "w") as stream:
        stream.write("<html><body><ul>")


def plot_data(evaluations):
    raw_scores_used_by_user(evaluations)
    raw_scores_used_by_user_per_use_case(evaluations)
    raw_scores_used_by_user_per_use_case_histograms(evaluations)
    plot_overall_method_performance(evaluations)
    plot_methods_per_user(evaluations)
    plot_methods_per_user_normalized(evaluations)
    plot_methods_per_use_case(evaluations)
    plot_methods_per_use_case_normalized(evaluations)
    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "jaccard: title",
        "nkod-title.udpipe-f.reduce.words_set.jaccard",
        "rgb(239, 85, 59)",
        "-jaccard-title-method-sort"
    )
    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "cosine: title [cswiki]",
        "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine",
        "rgb(254, 203, 82)",
        "-cosine-title-cswiki-method-sort"
    )
    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "jaccard: title",
        "nkod-title.udpipe-f.reduce.words_set.jaccard",
        "rgb(239, 85, 59)",
        "-jaccard-title",
        False
    )
    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "cosine: title [cswiki]",
        "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine",
        "rgb(254, 203, 82)",
        "-cosine-title-cswiki",
        False
    )


def on_plot_ready(figure, file_name, description):
    # figure.show()
    figure_path = os.path.join(OUTPUT_ROOT, file_name)
    if not os.path.exists(figure_path):
        figure.write_html(figure_path)
    with open(os.path.join(OUTPUT_ROOT, "index.html"), "a") as stream:
        stream.write(
            '<li><a href="./evaluation-reports-graphs/{}">{}</a></li>'.format(
                file_name, description))


def finalize_index():
    with open(os.path.join(OUTPUT_ROOT, "index.html"), "a") as stream:
        stream.write("</ul></body></html>")


def load_json(file: str):
    with open(file, "r", encoding="utf-8") as stream:
        return json.load(stream)


def raw_scores_used_by_user(evaluations):
    """
    Show values as used by users, for each value use total count it was used.
    A single value can be used multiple times in a single user-case.
    """
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(int))
    for evaluation in evaluations:
        for rating in evaluation["raw-rating"].values():
            data[evaluation["user"]][rating] += 1
    # Prepare plot data.
    figure = _create_figure_scores_per_user(
        data, "Absolute user ratings")
    on_plot_ready(figure, "user-ratings.html",
                  "For each user show how many times they have used "
                  "a given rating value.")


def _create_figure_scores_per_user(data, title):
    x_labels = sorted(data.keys())
    x = []
    y = []
    sizes = []
    for user, scores in data.items():
        for score, count in scores.items():
            x.append(x_labels.index(user))
            y.append(score)
            sizes.append(count)
    # Plot
    figure = plotly.express.scatter(x=x, y=y, size=sizes)
    figure.update_layout(
        title=title,
        xaxis_title=None,
        yaxis_title="Absolute user rating",
        xaxis={
            "tickmode": "array",
            "tickvals": list(range(len(x_labels))),
            "ticktext": x_labels,
        },
    )
    figure.update_traces(
        hovertemplate="Value %{y} <br>"
                      "Used %{marker.size} times"
                      "<extra></extra>"
    )
    return figure


def raw_scores_used_by_user_per_use_case(evaluations):
    """
    Modification of raw_scores_used_by_user
    Count only per use-case, i.e. max value is equal to number of use-cases.
    """
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(int))
    for evaluation in evaluations:
        for rating in set(evaluation["raw-rating"].values()):
            data[evaluation["user"]][rating] += 1
    # Prepare plot data.
    figure = _create_figure_scores_per_user(
        data, "Absolute user ratings per user-case")
    on_plot_ready(figure, "user-ratings-per-use-case.html",
                  "For each user show how in how many use-cases they "
                  "have used a given value.")


def raw_scores_used_by_user_per_use_case_histograms(evaluations):
    # df = plotly.express.data.tips()
    # counts, bins = numpy.histogram(df.total_bill, bins=range(0, 60, 5))
    # print("X", bins) [ 1 16 63 67 41 24 16  6  5  4  1] <- pocty
    # print("Y", counts) [ 0  5 10 15 20 25 30 35 40 45 50 55]
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(int))
    for evaluation in evaluations:
        used_values_count = len(set(evaluation["raw-rating"].values()))
        data[evaluation["user"]][used_values_count] += 1
    method_count = len(evaluations[0]["raw-rating"])
    x_ticks = list(range(method_count))
    # Prepare plot data.
    for user, usage in data.items():
        values = [
            usage.get(index, 0)
            for index in range(method_count)
        ]
        figure = plotly.graph_objs.Figure()
        figure.add_trace(plotly.graph_objs.Bar(
            y=values,
            x=list(range(method_count))
        ))
        figure.update_layout(
            title="Number of distinct ratings used per use-case "
                  "for '" + user + "'",
            showlegend=False,
            xaxis={
                "tickmode": "array",
                "tickvals": x_ticks,
                "ticktext": x_ticks,
            },
            xaxis_title="Number of used ratings",
            yaxis_title="How many times was rating used",
            yaxis_range=[0, method_count],
        )
        figure.update_traces(
            hovertemplate="%{x} values were used %{y} times"
                          "<extra></extra>"
        )
        on_plot_ready(figure,
                      "user-ratings-per-use-case-histogram-" + user + ".html",
                      "For " + user + " show how in how many use-cases they "
                                      "have used a given value.")


def plot_overall_method_performance(evaluations):
    data = collections.defaultdict(list)
    for evaluation in evaluations:
        for method, rating in evaluation["rating"].items():
            data[method].append(rating)
            pass
    # Plot
    figure = plotly.graph_objs.Figure()
    for method, ratings in data.items():
        figure.add_trace(plotly.graph_objs.Box(
            name=METHOD_LABELS[method],
            y=ratings
        ))
    figure.update_layout(
        title="Methods overall performance",
        yaxis_title="Relative user rating",
        showlegend=False,
    )
    on_plot_ready(figure, "methods-overall-performance.html",
                  "Show relative method performance as a box-plot using.")


def plot_methods_per_user(evaluations):
    users, lines = _prepare_method_per_user_data(evaluations)
    # Plot
    figure = _create_figure_rating_per_category(
        lines,
        title="Methods performance per user",
        y_title="Mean of relative user rating",
        y_ticks=users
    )
    on_plot_ready(figure, "methods-per-user-performance.html",
                  "Show how each method perform for given user.")


def _prepare_method_per_user_data(evaluations):
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    users = set()
    methods = set()
    for evaluation in evaluations:
        for method, rating in evaluation["rating"].items():
            users.add(evaluation["user"])
            methods.add(method)
            data[evaluation["user"]][method].append(rating)
    # Prepare plot data.
    users = sorted(list(users))
    methods = sorted(list(methods))
    lines = [{
        "data": [
            numpy.mean(data[user][method])
            for user in users
        ],
        "name": METHOD_LABELS[method]
    } for method in methods]
    return users, lines


def _create_figure_rating_per_category(lines, title, y_title, y_ticks):
    figure = plotly.graph_objs.Figure()
    for line in lines:
        figure.add_trace(plotly.graph_objs.Scatter(
            x=list(range(len(line["data"]))),
            y=line["data"],
            mode='lines+markers',
            name=line["name"],
            marker=dict(
                color=line.get("color", None)
            )
        ))
    figure.update_layout(
        title=title,
        xaxis_title=None,
        yaxis_title=y_title,
        showlegend=True,
        xaxis={
            "tickmode": "array",
            "tickvals": list(range(len(y_ticks))),
            "ticktext": y_ticks,
        },
    )
    figure.update_traces(
        hovertemplate="<b> %{data.name}</b> <br> "
                      "Value %{y:$.2f}"
                      "<extra></extra>",
    )
    return figure


def plot_methods_per_user_normalized(evaluations):
    """
    Update of plot_methods_per_user, users can have different maximum
    score, in this graph we make all max to be equal so the top method
    creates a line.
    """
    users, lines = _prepare_method_per_user_data(evaluations)
    normalized_lines = _normalize_lines_per_category(lines, users)
    # Plot
    figure = _create_figure_rating_per_category(
        normalized_lines,
        title="Normalized methods performance per user",
        y_title="Normalized mean of relative user rating",
        y_ticks=users
    )
    on_plot_ready(figure, "methods-per-user-performance-normalized.html",
                  "Show how each method perform for given user. The "
                  "performance for each method are normalized so the "
                  "best performing method has performance equal to 1.")


def _normalize_lines_per_category(lines, categories):
    max_values = [
        max([
            abs(line["data"][index])
            for line in lines
        ])
        for index in range(len(categories))
    ]
    return [
        {
            **line,
            "data": [
                value / max_value
                for value, max_value in zip(line["data"], max_values)
            ]
        }
        for line in lines
    ]


def plot_methods_per_use_case(evaluations):
    use_cases, lines = _prepare_plot_methods_per_use_case_data(evaluations)
    use_cases, lines = _order_lines_by_mean_decreasing(use_cases, lines)
    # Plot
    figure = _create_figure_rating_per_category(
        lines,
        title="Methods performance per user-case",
        y_title="Relative user rating",
        y_ticks=use_cases
    )
    on_plot_ready(figure, "methods-per-use-case-performance.html",
                  "Relative performance of methods by use-cases.")


def _order_lines_by_mean_decreasing(categories, lines):
    column_means = [
        (index,
         numpy.mean([
             line["data"][index]
             for line in lines
         ]))
        for index in range(len(categories))
    ]
    column_means.sort(key=lambda item: item[1], reverse=True)
    return [
               categories[index]
               for index, _ in column_means
           ], [
               {
                   **line,
                   "data": [
                       line["data"][index]
                       for index, _ in column_means
                   ],
               }
               for line in lines
           ]


def _prepare_plot_methods_per_use_case_data(evaluations):
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    use_cases = set()
    methods = set()
    for evaluation in evaluations:
        for method, rating in evaluation["rating"].items():
            use_cases.add(evaluation["use-case"])
            methods.add(method)
            data[evaluation["use-case"]][method].append(rating)
    # Prepare plot data.
    use_cases = sorted(list(use_cases), key=lambda value: int(value))
    methods = sorted(list(methods))
    lines = [
        {
            "data": [
                numpy.mean(data[user_case][method])
                for user_case in use_cases
            ],
            "name": METHOD_LABELS[method],
            "method": method
        }
        for method in methods
    ]
    return use_cases, lines


def plot_methods_per_use_case_normalized(evaluations):
    use_cases, lines = _prepare_plot_methods_per_use_case_data(evaluations)
    normalized_lines = _normalize_lines_per_category(lines, use_cases)
    use_cases, normalized_lines = _order_lines_by_mean_decreasing(
        use_cases, normalized_lines)
    # Plot
    figure = _create_figure_rating_per_category(
        normalized_lines,
        title="Normalized methods performance per user-case",
        y_title="Normalized relative user rating",
        y_ticks=use_cases
    )
    on_plot_ready(figure, "methods-per-use-case-performance-normalized.html",
                  "Relative performance of methods by use-cases. Performance "
                  "is normalized so on each use-case the best method have "
                  "performance equal to 1.")


def _order_lines_by_method_decreasing(categories, lines, method):
    """Order columns so the given method is in decreasing order."""
    ordering_line = _select_line_by_method(lines, method)
    ordering = [item for item in enumerate(ordering_line["data"])]
    ordering.sort(key=lambda item: item[1], reverse=True)
    return [
               categories[index]
               for index, _ in ordering
           ], [
               {
                   **line,
                   "data": [
                       line["data"][index]
                       for index, _ in ordering
                   ],
               }
               for line in lines
           ]


def _select_line_by_method(lines, method):
    for line in lines:
        if line["method"] == method:
            return line
    else:
        raise Exception("Missing method:" + method)


def plot_methods_per_use_case_normalized_for_method(
        evaluations, title, method, color, suffix, order_by_method=True):
    use_cases, lines = _prepare_plot_methods_per_use_case_data(evaluations)
    lines = _normalize_lines_per_category(lines, use_cases)
    if order_by_method:
        use_cases, lines = _order_lines_by_method_decreasing(
            use_cases, lines, method
        )
    else:
        use_cases, lines = _order_lines_by_mean_decreasing(use_cases, lines)
    # Set colors.
    for line in lines:
        line["color"] = "grey"
    method_line = _select_line_by_method(lines, method)
    method_line["color"] = color
    # Plot
    figure = _create_figure_rating_per_category(
        lines,
        title=title,
        y_title="Normalized relative user rating",
        y_ticks=use_cases
    )
    figure.update_layout(showlegend=False)
    on_plot_ready(figure,
                  "methods-per-use-case-performance-normalized"
                  + suffix + ".html",
                  "Normalized relative performance of methods by use-cases "
                  "for " + method + " sorted:" + str(order_by_method))


if __name__ == "__main__":
    main()

# TODO
#   ADD raw_scores_used_by_user but size = # use-case value is used in
#       -> absolute-user-ratings-per-use-case.html
# ADD raw_scores_used_by_user with relative scale,
#   ADD plot_method_ratings_per_user with relative scale normalized (max) for all users
#       -> methods-per-user-performance-normalized.html
# ADD for each user a histogram where  X 1-12 number of different values used in use case
#   DO Upload data to server
#       -> http://skoda.projekty.ms.mff.cuni.cz/www/gacr-2019/evaluation-reports-graphs/evaluation-reports-summary.json
#   ADD plot_methods_per_use_case with relative scale normalized (max) for x-values
#       -> plot_methods_per_use_case_normalized
#   UPDATE in methods per ... sort columns using average and selected method (gray out other methods)
#       -> methods-per-use-case-performance-normalized-jaccard-title-method-sort
#       -> methods-per-use-case-performance-normalized-cosine-title-cswiki-method-sort
#       -> methods-per-use-case-performance-normalized-jaccard-title
#       -> methods-per-use-case-performance-normalized-cosine-title-cswiki
#   CHECK "Methods performance" why no box plot for first
#       -> nkod-description.udpipe-f.reduce.hausdorff[law] gets no quartiles,
#          as the q1 and q3 values are zero. The quartiles using positions
#          in given sequence (as median).
# TODO ODIN
# Pridat tlacitko copy values to next in the evaluation view
#
