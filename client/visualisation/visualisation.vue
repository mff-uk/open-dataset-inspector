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
      :activeView="activeView"
    />
    <div style="bottom: 1rem; right: 2.5rem; position: fixed;">
      <v-row>
        <dialog-menu
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
    <path-dialog
      :visible="showPathDialog"
      :options="pathOptions"
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
import MappingFilterDialog from "./components/mapping-filter-dialog.vue";
import {
  ADD_DATASET,
  REMOVE_DATASET,
  SET_MAPPING_OPTIONS,
  SET_PATH_OPTIONS,
  GET_DATASETS,
  GET_LABELS,
  GET_NODES,
  GET_EDGES,
  GET_HIERARCHY,
  GET_NODES_PROPERTIES,
  GET_SIMILARITY_AVAILABLE,
  GET_SIMILARITY_PATHS,
} from "./visualisation-store";
import { SimilarityVisualisation } from "../similarity-visualisation";
import {
  createMappingFilters,
  createDefaultMappingOptions,
  createDefaultHighlightFilterOptions,
  createDefaultPathOptions,
} from "./visualisation-service.ts";
import SelectPathDialog from "./components/select-path-dialog.vue";
import HighlightDialog from "./components/highlight-filter-dialog.vue";
import DialogMenu from "./components/dialog-menu.vue";
import VisualisationMenu from "./components/visualisation-menu.vue";

export default {
  "name": "visualisation",
  "components": {
    "dataset-dialog": AddDatasetDialog,
    "network-visualisation": NetworkVisualisation,
    "similarity-visualisation": SimilarityVisualisation,
    "mapping-dialog": MappingFilterDialog,
    "path-dialog": SelectPathDialog,
    "highlight-dialog": HighlightDialog,
    "dialog-menu": DialogMenu,
    "visualisation-menu": VisualisationMenu,
  },
  "data": () => ({
    "showDatasetDialog": false,
    "showMappingDialog": false,
    "showPathDialog": false,
    "showHighlightDialog": false,
    //
    "activeView": 2,
    "mappingOptions": createDefaultMappingOptions(),
    "highlightOptions": createDefaultHighlightFilterOptions(),
    "pathOptions": createDefaultPathOptions(),
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
      this.pathOptions = options;
      this.$store.dispatch(SET_PATH_OPTIONS, {
        "leftDataset": this.datasets[0],
        "rightDataset": this.datasets[1],
        "options": options,
      });
    },
    "changeHighlightOptions": function (options) {
      this.showHighlightDialog = false;
      //
      this.highlightOptions = options;
    },
    "onSetLeftDataset": function (url, collection) {
      console.log("onSetLeftDataset", url, collection);
    },
    "onSetRightDataset": function (url, collection) {
      console.log("onSetRightDataset", url, collection);
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
