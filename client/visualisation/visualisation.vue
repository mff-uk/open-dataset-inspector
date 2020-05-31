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
      :paths="paths"
      :paths-are-available="pathsAreAvailable"
      @add-dataset="showDatasetDialog = true"
      @remove-dataset="onRemoveDataset"
    />
    <similarity-visualisation
      v-if="activeView > 0"
      :left-dataset="datasets[0]"
      :right-dataset="datasets[1]"
      :paths="paths"
      :labels="labels"
      :active-view="activeView"
    />
    <div style="bottom: 1rem; right: 2.5rem; position: fixed;">
      <v-row>
        <options-menu
          @show-mapping-dialog="showMappingDialog = true"
          @show-path-dialog="showPathDialog = true"
          @show-highlight-dialog="showHighlightDialog = true"
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
    <mapping-dialog
      :visible="showMappingDialog"
      :options="mappingOptions"
      @accept="changeMappingOptions"
      @reject="showMappingDialog = false"
    />
    <similarity-dialog
      :visible="showPathDialog"
      :options="similarityOptions"
      :dataset-count="datasets.length"
      @accept="changePathOptions"
      @reject="showPathDialog = false"
    />
    <highlight-dialog
      :visible="showHighlightDialog"
      :options="highlightOptions"
      @accept="changeHighlightOptions"
      @reject="showHighlightDialog = false"
    />
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

import NetworkVisualisation from "./network/network-visualisation.vue";
import AddDatasetDialog from "./components/add-dataset-dialog.vue";
import MappingFilterDialog from "./components/mapping-options-dialog.vue";
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
  GET_SIMILARITY_AVAILABLE,
  GET_SIMILARITY_PATHS,
  GET_SIMILARITY_OPTIONS,
} from "./visualisation-store";
import { SimilarityVisualisation } from "../similarity-visualisation";
import {
  createMappingFilters,
  createDefaultMappingOptions,
  createDefaultHighlightFilterOptions,
} from "./visualisation-service.ts";
import SimilarityDialog from "./components/similarity-options-dialog.vue";
import HighlightDialog from "./components/highlight-options-dialog.vue";
import OptionsMenu from "./components/options-menu.vue";
import VisualisationMenu from "./components/visualisation-menu.vue";

export default {
  "name": "visualisation",
  "components": {
    "dataset-dialog": AddDatasetDialog,
    "network-visualisation": NetworkVisualisation,
    "similarity-visualisation": SimilarityVisualisation,
    "mapping-dialog": MappingFilterDialog,
    "similarity-dialog": SimilarityDialog,
    "highlight-dialog": HighlightDialog,
    "options-menu": OptionsMenu,
    "visualisation-menu": VisualisationMenu,
  },
  "data": () => ({
    "showDatasetDialog": false,
    "showMappingDialog": false,
    "showPathDialog": false,
    "showHighlightDialog": false,
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
      "paths": GET_SIMILARITY_PATHS,
      "similarityOptions": GET_SIMILARITY_OPTIONS,
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
    "onRemoveDataset": function (dataset) {
      this.$store.dispatch(REMOVE_DATASET, dataset);
    },
    "onSetPaths": function () {
      this.showPathDialog = true;
    },
    "changePathOptions": function (options) {
      this.showPathDialog = false;
      //
      this.$store.dispatch(SET_SIMILARITY_OPTIONS, options);
      if (this.datasets.length === 2) {
        this.$store.dispatch(FETCH_SIMILARITY, {
          "datasets": [this.datasets[0], this.datasets[1]],
        });
      }
    },
    "changeHighlightOptions": function (options) {
      this.showHighlightDialog = false;
      //
      this.highlightOptions = options;
    },
    "changeMappingOptions": function (options) {
      this.showMappingDialog = false;
      //
      this.mappingOptions = options;
      this.$store.dispatch(
        SET_MAPPING_OPTIONS,
        createMappingFilters(this.mappingOptions)
      );
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
