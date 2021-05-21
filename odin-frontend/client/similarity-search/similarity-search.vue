<template>
  <v-container fluid>
    <query-panel
      :query="query"
      :methods="methodsList"
      @search="onSearch"
    />
    <br>
    <query-dataset-detail
      label="Query datasets"
      :languages="languages"
      :datasets="queryDatasets"
    />
    <br>
    <query-dataset-detail
      label="Expected datasets"
      :languages="languages"
      :datasets="expectedDatasets"
    />
    <br>
    <method-array
      :query="query.dataset"
      :datasets="datasets"
      :methods="methods"
      :similar="similar"
      :expected="expectedResults"
      :languages="languages"
    />
  </v-container>
</template>

<script>
import MethodArray from "./method-array.vue";
import DatasetDetail from "./dataset-detail.vue";
import QueryPanel from "./query-panel.vue";
import { fetchSimilarityMethods } from "../app-service/similarity-api.ts";
import {
  getSimilarDatasets,
  getDatasetsPositions,
} from "../app-service/similarity-service.ts";

export default {
  "name": "evaluation",
  "components": {
    "method-array": MethodArray,
    "query-dataset-detail": DatasetDetail,
    "query-panel": QueryPanel,
  },
  "data": () => ({
    // Active query, can be loaded from URL.
    "query": {
      "dataset": [],
      "expected": [],
      "method": [],
    },
    // Other.
    "languages": ["en", "cs"],
    // All dataset metadata, like title, description, etc..
    "datasets": {},
    // Methods metadata.
    "methods": {},
    "methodsList": [],
    // For given method contains list of founded datasets.
    "similar": {},
    // For given method contains list of positions of expected datasets.
    "expectedResults": {},
  }),
  "computed": {
    "queryDatasets": function () {
      return this.query.dataset
        .map((iri) => this.datasets[iri] || { "iri": iri });
    },
    "expectedDatasets": function () {
      return this.query.expected
        .map((iri) => this.datasets[iri] || { "iri": iri });
    },
  },
  "mounted": function () {
    this.query = {
      "dataset": asArray(this.$route.query.dataset || []),
      "expected": asArray(this.$route.query.expected || []),
      "method": asArray(this.$route.query.method || []),
      "count": this.$route.query.count || 3,
    };
    this.fetchData();
  },
  "methods": {
    "fetchData": async function () {
      this.methods = await fetchSimilarityMethods();
      this.methodsList = Object.values(this.methods);
      if (this.query.dataset.length === 0) {
        return;
      }
      const methods = this.query.method
        .map((id) => this.methods[id])
        .filter((item) => item !== undefined);
      const options = {
        "count": this.query.count,
      };
      // Similar datasets.
      const similar = await getSimilarDatasets(
        methods, this.query.dataset, options
      );
      this.datasets = similar.datasets;
      this.similar = similar.similar;
      // Expected datasets.
      if (this.query.expected.length > 0) {
        this.expectedResults = await getDatasetsPositions(
          methods, this.query.dataset, this.query.expected
        );
      } else {
        this.expectedResults = {};
      }
    },
    "onSearch": function (query) {
      this.$router.push({
        "path": "search",
        "query": {
          ...this.$route.query,
          "dataset": query.dataset,
          "expected": query.expected,
          "method": query.method,
        },
      });
      this.query = query;
      this.fetchData();
    },
    // "onLoadMore": function (method) {
    //   const options = {
    //     ...this.getFetchOptions(),
    //     "count": method.datasets.length + 10,
    //   };
    //   const queryIris = datasetStringToArray(this.query.dataset);
    //   const knownDatasets = Object.keys(this.datasets);
    //   fetchMoreForMethod(method.id, queryIris, knownDatasets, options)
    //     .then((result) => {
    //       // Copy array and replace the one index.
    //       this.methods = [...this.methods];
    //       for (const index in this.methods) {
    //         if (!Object.prototype.hasOwnProperty.call(this.methods, index)) {
    //           continue;
    //         }
    //         if (this.methods[index].id === result.method.id) {
    //           this.methods[index] = result.method;
    //           break;
    //         }
    //       }
    //       // Add new datasets.
    //       this.datasets = {
    //         ...this.datasets,
    //         ...result.datasets,
    //       };
    //     });
  },
};

function asArray(value) {
  return Array.isArray(value) ? value : [value];
}

</script>
