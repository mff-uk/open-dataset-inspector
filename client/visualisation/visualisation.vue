<template>
  <v-container
    style="height: 100%"
    fluid
  >
    <network-visualisation
      v-if="activeView === 0"
      :datasets="datasets"
      :nodes="nodes"
      :edges="edges"
      :labels="labels"
      @add-dataset="onAddDataset"
      @remove-dataset="onRemoveDataset"
    />
    <vis-container
      v-if="activeView === 1"
      :left-dataset="datasets[0]"
      :right-dataset="datasets[1]"
      @pathsChanged="onSetPaths"
    />
    <dataset-dialog
      v-model="datasetDialogVisible"
      @add-dataset="addDataset"
      @leftDatasetChanged="onSetLeftDataset"
      @rightDatasetChanged="onSetRightDataset"
    />
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

import NetworkVisualisation from "./network/network-visualisation.vue";
import AddDatasetDialog from "./add-dataset-dialog.vue";
import {
  ADD_DATASET,
  GET_DATASETS,
  GET_LABELS,
  GET_NODES,
  GET_EDGES,
  GET_HIERARCHY,
} from "./visualisation-store";
import { VisContainer } from "../similarity-visualisation";

export default {
  "name": "visualisation",
  "components": {
    "dataset-dialog": AddDatasetDialog,
    "network-visualisation": NetworkVisualisation,
    "vis-container": VisContainer,
  },
  "data": () => ({
    "datasetDialogVisible": false,
    "activeView": 1,
  }),
  "computed": {
    ...mapGetters("hierarchy", {
      "datasets": GET_DATASETS,
      "nodes": GET_NODES,
      "edges": GET_EDGES,
      "labels": GET_LABELS,
      "hierarchy": GET_HIERARCHY,
    }),
  },
  "mounted": function () {
    if (this.$route.query.dataset && this.$route.query.collection) {
      this.$route.query.dataset.forEach((url) => {
        this.$store.dispatch(
          ADD_DATASET, {
            "url": url,
            "collection": this.$route.query.collection,
          }
        );
      });
    }
  },
  "methods": {
    "onAddDataset": function () {
      this.datasetDialogVisible = true;
    },
    "onRemoveDataset": function (index) {
      console.log("TODO onRemoveDataset", index);
    },
    "onSetPaths": function (name) {
      console.log("TODO onSetPath", name);
    },
    "addDataset": function (dataset) {
      this.$store.dispatch(ADD_DATASET, dataset);
    },
    "onSetLeftDataset": function (url, collection) {
      console.log("onSetLeftDataset", url, collection);
    },
    "onSetRightDataset": function (url, collection) {
      console.log("onSetRightDataset", url, collection);
    },
  },
};
</script>
