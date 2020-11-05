#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import os

import numpy

import plotly
import plotly.express

# Change to your local setting!
plotly.io.orca.config.executable = "C:/Users/Petr/AppData/Local/Programs/orca/orca.exe"

OUTPUT_ROOT = "../data/evaluation-reports-graphs/20201015"

SIMILARITY_DASH = {
    "hausdorff": "dash",
    "cosine": "dot",
    "jaccard": "dashdot"
}

DESCRIPTOR_COLOR = {
    "description [cswiki]": "#ff0000",
    "description [law]": "#00ff00",
    "description": "#c71585",
    "keywords": "#6c6c00",
    "title [cswiki]": "#0000ff",
    "title [law]": "#1e90ff",
    "title": "#ffd700"
}

METHOD_METADATA = {
    "nkod-_title_description_.join.reduce.tlsh.tlsh": {
        "label": "tlsh : title description",
        "color": "black",
        "dash": None,
        "mode": "lines",
    },
    "nkod-description.udpipe-f.reduce.hausdorff[cswiki]": {
        "label": "hausdorff : description [cswiki]",
        "color": DESCRIPTOR_COLOR["description [cswiki]"],
        "dash": SIMILARITY_DASH["hausdorff"],
    },
    "nkod-description.udpipe-f.reduce.hausdorff[law]": {
        "label": "hausdorff : description [law]",
        "color": DESCRIPTOR_COLOR["description [law]"],
        "dash": SIMILARITY_DASH["hausdorff"],
    },
    "nkod-description.udpipe-f.reduce.word2vec[cswiki].vector.cosine": {
        "label": "cosine : description [cswiki]",
        "color": DESCRIPTOR_COLOR["description [cswiki]"],
        "dash": SIMILARITY_DASH["cosine"],
    },
    "nkod-description.udpipe-f.reduce.word2vec[law].vector.cosine": {
        "label": "cosine : description [law]",
        "color": DESCRIPTOR_COLOR["description [law]"],
        "dash": SIMILARITY_DASH["cosine"],
    },
    "nkod-description.udpipe-f.reduce.words_count.cosine": {
        "label": "cosine : description",
        "color": DESCRIPTOR_COLOR["description"],
        "dash": SIMILARITY_DASH["cosine"],
    },
    "nkod-keywords.concat.reduce.set.jaccard": {
        "label": "jaccard : keywords",
        "color": DESCRIPTOR_COLOR["keywords"],
        "dash": SIMILARITY_DASH["jaccard"],
    },
    "nkod-title.udpipe-f.reduce.hausdorff[cswiki]": {
        "label": "hausdorff : title [cswiki]",
        "color": DESCRIPTOR_COLOR["title [cswiki]"],
        "dash": SIMILARITY_DASH["hausdorff"],
    },
    "nkod-title.udpipe-f.reduce.hausdorff[law]": {
        "label": "hausdorff : title [law]",
        "color": DESCRIPTOR_COLOR["title [law]"],
        "dash": SIMILARITY_DASH["hausdorff"],
    },
    "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine": {
        "label": "cosine : title [cswiki]",
        "color": DESCRIPTOR_COLOR["title [cswiki]"],
        "dash": SIMILARITY_DASH["cosine"],
    },
    "nkod-title.udpipe-f.reduce.word2vec[law].vector.cosine": {
        "label": "cosine : title [law]",
        "color": DESCRIPTOR_COLOR["title [law]"],
        "dash": SIMILARITY_DASH["cosine"],
    },
    "nkod-title.udpipe-f.reduce.words_set.jaccard": {
        "label": "jaccard : title",
        "color": DESCRIPTOR_COLOR["title"],
        "dash": SIMILARITY_DASH["jaccard"],
    },
}

PLOT_EXTENSION = "pdf"


def main():
    evaluations = load_json(
        "../data/evaluation-reports-archive/"
        "20200621-evaluation-reports-summary.json"
    )
    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    prepare_index()
    plot_data_iiwas(evaluations)
    # plot_data(evaluations)
    finalize_index()


def prepare_index():
    with open(os.path.join(OUTPUT_ROOT, "index.html"), "w") as stream:
        stream.write("<html><body><ul>")


def plot_data_iiwas(evaluations):
    def map_use_case(usecase):
        return "S" + usecase

    def map_user(user):
        return {
            "Martin": "U1",
            "Kuba": "U2",
            "PeSk": "U3",
            "DaBe": "U4",
            "1978": "U5"
        }[user]

    raw_scores_used_by_user_per_use_case(evaluations, map_user)
    plot_overall_method_performance(evaluations)
    plot_methods_per_user_normalized(evaluations, map_user)
    plot_methods_per_use_case_normalized(evaluations, map_use_case)

    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "jaccard: title",
        "nkod-title.udpipe-f.reduce.words_set.jaccard",
        "-jaccard-title",
        map_use_case,
        False
    )

    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "cosine: title [cswiki]",
        "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine",
        "-cosine-title-cswiki",
        map_use_case,
        False
    )


def plot_data(evaluations):
    def map_use_case(usecase):
        return "S" + usecase

    def map_user(user):
        return {
            "Martin": "U1",
            "Kuba": "U2",
            "PeSk": "U3",
            "DaBe": "U4",
            "1978": "U5"
        }[user]

    raw_scores_used_by_user(evaluations, map_user)
    raw_scores_used_by_user_per_use_case_histograms(evaluations, map_user)

    plot_methods_per_user(evaluations, map_user)
    plot_methods_per_use_case(evaluations, map_use_case)

    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "jaccard: title",
        "nkod-title.udpipe-f.reduce.words_set.jaccard",
        "rgb(239, 85, 59)",
        "-jaccard-title-method-sort",
        map_use_case
    )
    plot_methods_per_use_case_normalized_for_method(
        evaluations,
        "Normalized methods performance per user-case for "
        + "cosine: title [cswiki]",
        "nkod-title.udpipe-f.reduce.word2vec[cswiki].vector.cosine",
        "rgb(254, 203, 82)",
        "-cosine-title-cswiki-method-sort",
        map_use_case
    )


def on_plot_ready(figure, file_name, description, width=1024, height=768):
    figure_path = os.path.join(OUTPUT_ROOT, file_name)
    figure.write_image(
        figure_path + "." + PLOT_EXTENSION,
        width=width,
        height=height)
    # Save as HTML file to allow web-based browsing of the data.
    if not os.path.exists(figure_path + ".html"):
        figure.write_html(figure_path + ".html")
    with open(os.path.join(OUTPUT_ROOT, "index.html"), "a") as stream:
        stream.write(
            '<li><a href="./evaluation-reports-graphs/{}">{}</a></li>'.format(
                file_name + ".html", description))


def finalize_index():
    with open(os.path.join(OUTPUT_ROOT, "index.html"), "a") as stream:
        stream.write("</ul></body></html>")


def load_json(file: str):
    with open(file, "r", encoding="utf-8") as stream:
        return json.load(stream)


def raw_scores_used_by_user(evaluations, map_user):
    """
    Show values as used by users, for each value use total count it was used.
    A single value can be used multiple times in a single user-case.
    """
    # Collect data.
    data = collections.defaultdict(lambda: collections.Counter())
    for evaluation in evaluations:
        user = map_user(evaluation["user"])
        data[user].update(
            collections.Counter(evaluation["raw-rating"].values()))
    # Prepare plot data.
    figure = _create_figure_scores_per_user(
        data, "Absolute ranking category")
    on_plot_ready(figure, "user-ratings",
                  "For each user show how many times they have used "
                  "a given ranking value.")


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
        # title=title,
        xaxis=dict(
            title=None,
            tickmode="array",
            tickvals=list(range(len(x_labels))),
            ticktext=x_labels,
            tickfont=dict(size=24),
        ),
        yaxis=dict(
            title="Absolute user ranking",
            tickfont=dict(size=24),
            titlefont=dict(size=28),
        ),
        margin=dict(l=0, r=20, t=5, b=25),
    )
    figure.update_traces(
        hovertemplate="Value %{y} <br>"
                      "Used %{marker.size} times"
                      "<extra></extra>",
        marker=dict(
            color="gray",
            line=dict(color="gray")
        )
    )
    return figure


def raw_scores_used_by_user_per_use_case(evaluations, map_user):
    """
    Modification of raw_scores_used_by_user
    Count only per use-case, i.e. max value is equal to number of use-cases.
    Y - ranking used by user, 0 is the best
    """
    # Collect data.
    data = collections.defaultdict(lambda: collections.Counter())
    for evaluation in evaluations:
        user = map_user(evaluation["user"])
        data[user].update(
            collections.Counter(set(evaluation["raw-rating"].values())))
    # Prepare plot data.
    figure = _create_figure_scores_per_user(
        data, "Absolute user rankings per user-case")
    on_plot_ready(
        figure,
        "user-ratings-per-use-case",
        "For each user show how in how many use-cases they "
        "have used a given value.",
        height=1024)


def raw_scores_used_by_user_per_use_case_histograms(evaluations, map_user):
    # df = plotly.express.data.tips()
    # counts, bins = numpy.histogram(df.total_bill, bins=range(0, 60, 5))
    # print("X", bins) [ 1 16 63 67 41 24 16  6  5  4  1] <- pocty
    # print("Y", counts) [ 0  5 10 15 20 25 30 35 40 45 50 55]
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(int))
    for evaluation in evaluations:
        used_values_count = len(set(evaluation["raw-rating"].values()))
        user = map_user(evaluation["user"])
        data[user][used_values_count] += 1
    method_count = len(evaluations[0]["raw-rating"]) + 1
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
            title="Number of distinct rankings used per use-case "
                  "for '" + user + "'",
            showlegend=False,
            xaxis={
                "tickmode": "array",
                "tickvals": x_ticks,
                "ticktext": x_ticks,
            },
            xaxis_title="Number of used rankings",
            yaxis_title="How many times was ranking used",
            yaxis_range=[0, method_count],
        )
        figure.update_traces(
            hovertemplate="%{x} values were used %{y} times"
                          "<extra></extra>"
        )
        on_plot_ready(
            figure,
            "user-ratings-per-use-case-histogram-" + user + "",
            "For " + user + " show how in how many use-cases they "
                            "have used a given value.",
            height=1024)


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
            name=METHOD_METADATA[method]["label"],
            y=ratings,
            line=dict(color="gray")
        ))
    figure.update_layout(
        # title="Methods overall performance",
        yaxis=dict(
            title="Relative user ranking",
            tickfont=dict(size=24),
            titlefont=dict(size=28),
        ),
        xaxis=dict(
            tickfont=dict(size=24),
            tickangle=90,
        ),
        showlegend=False,
        margin=dict(l=0, r=20, t=5, b=25),
    )
    on_plot_ready(
        figure,
        "methods-overall-performance",
        "Show relative method performance as a box-plot using.",
        height=1024)


def plot_methods_per_user(evaluations, map_user):
    users, lines = _prepare_method_per_user_data(evaluations, map_user)
    # Plot
    figure = _create_figure_rating_per_category(
        lines,
        title="Methods performance per user",
        y_title="Mean of relative user ranking",
        y_ticks=users
    )
    on_plot_ready(
        figure,
        "methods-per-user-performance",
        "Show how each method perform for given user.",
        height=1024)


def _prepare_method_per_user_data(evaluations, map_user):
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    users = set()
    methods = set()
    for evaluation in evaluations:
        for method, rating in evaluation["rating"].items():
            user = map_user(evaluation["user"])
            users.add(user)
            methods.add(method)
            data[user][method].append(rating)
    # Prepare plot data.
    users = sorted(list(users))
    methods = sorted(list(methods))
    lines = [{
        "data": [
            numpy.mean(data[user][method])
            for user in users
        ],
        "metadata": METHOD_METADATA[method],
        "method": method
    } for method in methods]
    return users, lines


def _create_figure_rating_per_category(lines, title, y_title, y_ticks):
    figure = plotly.graph_objs.Figure()
    for line in lines:
        figure.add_trace(plotly.graph_objs.Scatter(
            x=list(range(len(line["data"]))),
            y=line["data"],
            mode=line["metadata"].get("mode", "lines+markers"),
            name=line["metadata"]["label"],
            line=dict(
                color=line["metadata"].get("color", None),
                dash=line["metadata"].get("dash"),
            ),
        ))
    figure.update_layout(
        # title=title,
        showlegend=True,
        xaxis=dict(
            title=None,
            tickmode="array",
            tickvals=list(range(len(y_ticks))),
            ticktext=y_ticks,
            tickfont=dict(size=24),
        ),
        yaxis=dict(
            title=y_title,
            tickfont=dict(size=24),
            titlefont=dict(size=28),
        ),
        legend=dict(
            orientation="h",
            font=dict(size=24),
        ),
        margin=dict(l=0, r=20, t=5, b=25),
    )
    figure.update_traces(
        hovertemplate="<b> %{data.name}</b> <br> "
                      "Value %{y:$.2f}"
                      "<extra></extra>",
    )
    return figure


def plot_methods_per_user_normalized(evaluations, map_user):
    """
    Update of plot_methods_per_user, users can have different maximum
    score, in this graph we make all max to be equal so the top method
    creates a line.
    """
    users, lines = _prepare_method_per_user_data(evaluations, map_user)
    normalized_lines = _normalize_lines_per_category(lines, users)
    # Plot
    figure = _create_figure_rating_per_category(
        normalized_lines,
        title="Normalized methods performance per user",
        y_title="Relative method ranking",
        y_ticks=users
    )
    on_plot_ready(figure, "methods-per-user-performance-normalized",
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


def plot_methods_per_use_case(evaluations, map_use_case):
    use_cases, lines = \
        _prepare_plot_methods_per_use_case_data(evaluations, map_use_case)
    use_cases, lines = _order_lines_by_mean_decreasing(use_cases, lines)
    # Plot
    figure = _create_figure_rating_per_category(
        lines,
        title="Methods performance per user-case",
        y_title="Relative user ranking",
        y_ticks=use_cases
    )
    on_plot_ready(figure, "methods-per-use-case-performance",
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


def _prepare_plot_methods_per_use_case_data(evaluations, map_use_case):
    # Collect data.
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    use_cases = set()
    methods = set()
    for evaluation in evaluations:
        for method, rating in evaluation["rating"].items():
            use_case = map_use_case(evaluation["use-case"])
            use_cases.add(use_case)
            methods.add(method)
            data[use_case][method].append(rating)
    # Prepare plot data.
    use_cases = sorted(list(use_cases), key=lambda value: value)
    methods = sorted(list(methods))
    lines = [
        {
            "data": [
                numpy.mean(data[user_case][method])
                for user_case in use_cases
            ],
            "method": method,
            "metadata": METHOD_METADATA[method],
        }
        for method in methods
    ]
    return use_cases, lines


def plot_methods_per_use_case_normalized(evaluations, map_use_case):
    use_cases, lines = \
        _prepare_plot_methods_per_use_case_data(evaluations, map_use_case)
    normalized_lines = _normalize_lines_per_category(lines, use_cases)
    use_cases, normalized_lines = _order_lines_by_mean_decreasing(
        use_cases, normalized_lines)
    # Plot
    figure = _create_figure_rating_per_category(
        normalized_lines,
        title="Normalized methods performance per user-case",
        y_title="Relative method ranking",
        y_ticks=use_cases
    )
    on_plot_ready(
        figure,
        "methods-per-use-case-performance-normalized",
        "Relative performance of methods by use-cases. Performance "
        "is normalized so on each use-case the best method have "
        "performance equal to 1.",
        height=1024)


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
        evaluations, title, method, suffix,
        map_use_case, order_by_method=True):
    use_cases, lines = \
        _prepare_plot_methods_per_use_case_data(evaluations, map_use_case)
    lines = _normalize_lines_per_category(lines, use_cases)
    if order_by_method:
        use_cases, lines = _order_lines_by_method_decreasing(
            use_cases, lines, method
        )
    else:
        use_cases, lines = _order_lines_by_mean_decreasing(use_cases, lines)
    # Set colors.
    for line in lines:
        if line["method"] == method:
            continue
        line["metadata"] = {
            **line["metadata"],
            "color": "grey"
        }
    # Plot
    figure = _create_figure_rating_per_category(
        lines,
        title=title,
        y_title="Relative method ranking",
        y_ticks=use_cases
    )
    figure.update_layout(showlegend=False)
    on_plot_ready(
        figure,
        "methods-per-use-case-performance-normalized"
        + suffix + "",
        "Normalized relative performance of methods by use-cases "
        "for " + method + " sorted:" + str(order_by_method),
        width=1024)


if __name__ == "__main__":
    main()
