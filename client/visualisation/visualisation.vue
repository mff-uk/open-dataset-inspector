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
      :nodes-properties="nodesProperties"
      :highlight-options="highlightOptions"
      :paths-are-available="pathsAreAvailable"
      :similarity="similarity"
      :similarity-options="similarityOptions"
      @add-dataset="showDatasetDialog = true"
      @remove-dataset="onRemoveDataset"
      @show-similarity-dialog="onShowSimilarityDialog"
    />
    <similarity-visualisation
      v-if="activeView > 0"
      :left-dataset="datasets[0]"
      :right-dataset="datasets[1]"
      :paths="similarity === undefined ? [] : similarity.paths"
      :labels="labels"
      :active-view="activeView"
    />
    <div style="bottom: 1rem; right: 2.5rem; position: fixed;">
      <v-row>
        <options-menu
          @show-options-dialog="showOptionsDialog = true"
        />
        &nbsp;
        <visualisation-menu
          v-model="activeView"
        />
      </v-row>
    </div>
    <dataset-dialog
      :visible="showDatasetDialog"
      @accept="addDataset"
      @reject="showDatasetDialog = false"
    />
    <options-dialog
      ref="optionsDialog"
      :visible="showOptionsDialog"
      :highlight="highlightOptions"
      :mapping="mappingOptions"
      :similarity="similarityOptions"
      :dataset-count="datasets.length"
      @accept="onChangeOptions"
      @reject="showOptionsDialog = false"
    />
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

import NetworkVisualisation from "./network/network-visualisation.vue";
import AddDatasetDialog from "./components/add-dataset-dialog.vue";
import {
  ADD_DATASET,
  REMOVE_DATASET,
  SET_MAPPING_OPTIONS,
  SET_SIMILARITY_OPTIONS,
  FETCH_SIMILARITY,
  GET_DATASETS,
  GET_LABELS,
  GET_NODES,
  GET_EDGES,
  GET_HIERARCHY,
  GET_NODES_PROPERTIES,
  GET_SIMILARITY,
  GET_SIMILARITY_AVAILABLE,
  GET_SIMILARITY_OPTIONS,
} from "./visualisation-store";
import { SimilarityVisualisation } from "../similarity-visualisation";
import {
  createMappingFilters,
  createDefaultMappingOptions,
  createDefaultHighlightFilterOptions,
} from "./visualisation-service.ts";
import OptionsDialog from "./components/options-dialog.vue";
import OptionsMenu from "./components/options-menu.vue";
import VisualisationMenu from "./components/visualisation-menu.vue";

export default {
  "name": "visualisation",
  "components": {
    "dataset-dialog": AddDatasetDialog,
    "network-visualisation": NetworkVisualisation,
    "similarity-visualisation": SimilarityVisualisation,
    "options-dialog": OptionsDialog,
    "options-menu": OptionsMenu,
    "visualisation-menu": VisualisationMenu,
  },
  "data": () => ({
    "showDatasetDialog": false,
    "showOptionsDialog": false,
    //
    "activeView": 0,
    "mappingOptions": createDefaultMappingOptions(),
    "highlightOptions": createDefaultHighlightFilterOptions(),
  }),
  "computed": {
    ...mapGetters("hierarchy", {
      "datasets": GET_DATASETS,
      "nodes": GET_NODES,
      "edges": GET_EDGES,
      "labels": GET_LABELS,
      "hierarchy": GET_HIERARCHY,
      "nodesProperties": GET_NODES_PROPERTIES,
      "pathsAreAvailable": GET_SIMILARITY_AVAILABLE,
      "similarityOptions": GET_SIMILARITY_OPTIONS,
      "similarity": GET_SIMILARITY,
    }),
  },
  "mounted": function () {
    this.$store.dispatch(
      SET_MAPPING_OPTIONS,
      createMappingFilters(this.mappingOptions)
    );
    //
    if (this.$route.query.dataset && this.$route.query.collection) {
      asArray(this.$route.query.dataset).forEach((url) => {
        this.$store.dispatch(
          ADD_DATASET, {
            "dataset": url,
            "collection": this.$route.query.collection,
          }
        );
      });
    }
  },
  "methods": {
    "addDataset": function (dataset) {
      this.showDatasetDialog = false;
      //
      this.$store.dispatch(ADD_DATASET, dataset);
    },
    "onShowSimilarityDialog": function () {
      this.$refs.optionsDialog.setTab(2);
      this.showOptionsDialog = true;
    },
    "onRemoveDataset": function (dataset) {
      this.$store.dispatch(REMOVE_DATASET, dataset);
    },
    "onChangeOptions": function (event) {
      this.showOptionsDialog = false;
      //
      this.$store.dispatch(SET_SIMILARITY_OPTIONS, event.similarity);
      if (this.datasets.length === 2) {
        this.$store.dispatch(FETCH_SIMILARITY, {
          "datasets": [this.datasets[0], this.datasets[1]],
        });
      }
      //
      this.mappingOptions = event.mapping;
      this.$store.dispatch(
        SET_MAPPING_OPTIONS,
        createMappingFilters(this.mappingOptions)
      );
      //
      this.highlightOptions = event.highlight;
    },
  },
};

function asArray(value) {
  if (Array.isArray(value)) {
    return value;
  }
  return [value];
}

</script>
