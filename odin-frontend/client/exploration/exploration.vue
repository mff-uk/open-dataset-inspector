<template>
  <v-container fluid>
    <query-panel
      :query="query"
      :description="description"
      @search="onSearch"
    />
    <br>
    <query-dataset-detail
      label="Query datasets"
      :datasets="queryDatasets"
    />
    <br>
    <query-dataset-detail
      label="Expected datasets"
      :datasets="expectedDatasets"
    />
    <br>
    <method-array
      :datasets="datasets"
      :methods="methods"
      :highlights="highlights"
      :expected="expectedPositions"
      @load-more="onLoadMore"
    />
  </v-container>
</template>

<script>
import MethodArray from "./method-array.vue";
import DatasetDetail from "./dataset-detail.vue";
import QueryPanel from "./query-panel.vue";
import {
  fetchSimilarDatasets,
  fetchDatasets,
  fetchMoreForMethod,
  fetchDatasetsPositions,
} from "../evaluation/evaluation-service.ts";
import {
  queryParamsToDatasetString,
  datasetStringToArray,
} from "../utils.ts";

export default {
  "name": "evaluation",
  "components": {
    "method-array": MethodArray,
    "query-dataset-detail": DatasetDetail,
    "query-panel": QueryPanel,
  },
  "data": () => ({
    "query": {
      "dataset": "",
      "group": "",
      "expected": "",
      "fusion": "min",
    },
    "datasets": {},
    "methods": [],
    "description": "",
    "highlights": {},
    "queryIris": [],
    "expectedIris": [],
    "expectedPositions": {},
  }),
  "computed": {
    "queryDatasets": function () {
      return this.queryIris
        .map((iri) => this.datasets[iri] || { "iri": iri });
    },
    "expectedDatasets": function () {
      return this.expectedIris
        .map((iri) => this.datasets[iri] || { "iri": iri });
    },
  },
  "mounted": function () {
    this.query = {
      "dataset": queryParamsToDatasetString(this.$route.query.dataset),
      "group": this.$route.query.group || "group-000",
      "expected": queryParamsToDatasetString(this.$route.query.expected),
      "fusion": this.$route.query.fusion || "min",
    };
    this.load();
  },
  "methods": {
    "load": function () {
      const options = {
        ...this.getFetchOptions(),
        "count": this.$route.query.count || 3,
      };
      // Update all the data.
      this.methods = [];
      this.datasets = {};
      this.queryIris = datasetStringToArray(this.query.dataset);
      this.expectedIris = datasetStringToArray(this.query.expected);
      this.highlights = {};
      for (const iri of this.expectedIris) {
        this.highlights[iri] = "#90EE90";
      }
      this.expectedPositions = {};
      // Check if we have data for fetch.
      if (this.query.group === "") {
        return;
      }
      // Fetch.
      fetchSimilarDatasets(this.query.group, this.queryIris, options)
        .then((result) => {
          this.methods = result.methods;
          this.datasets = {
            ...this.datasets,
            ...result.datasets,
          };
          this.description = result.description;
          this.ratings = {};
        });
      fetchDatasets(this.expectedIris)
        .then((result) => {
          this.datasets = {
            ...this.datasets,
            ...result,
          };
        });
      fetchDatasetsPositions(
        this.query.group, this.queryIris, this.expectedIris, options.fustion
      ).then((result) => {
        this.expectedPositions = result;
      });
    },
    "getFetchOptions": function () {
      return {
        "fusion": this.query.fusion,
      };
    },
    "onSearch": function (search) {
      this.query = {
        ...this.query,
        ...search,
      };
      const dataset = datasetStringToArray(search.dataset);
      const expected = datasetStringToArray(search.expected);
      this.$router.push({
        "path": "exploration",
        "query": {
          ...this.$route.query,
          ...this.query,
          "dataset": dataset,
          "expected": expected,
        },
      });
      this.load();
    },
    "onLoadMore": function (method) {
      const options = {
        ...this.getFetchOptions(),
        "count": method.datasets.length + 10,
      };
      const queryIris = datasetStringToArray(this.query.dataset);
      const knownDatasets = Object.keys(this.datasets);
      fetchMoreForMethod(method.id, queryIris, knownDatasets, options)
        .then((result) => {
          // Copy array and replace the one index.
          this.methods = [...this.methods];
          for (const index in this.methods) {
            if (!Object.prototype.hasOwnProperty.call(this.methods, index)) {
              continue;
            }
            if (this.methods[index].id === result.method.id) {
              this.methods[index] = result.method;
              break;
            }
          }
          // Add new datasets.
          this.datasets = {
            ...this.datasets,
            ...result.datasets,
          };
        });
    },
  },
};

</script>

<style>
</style>
