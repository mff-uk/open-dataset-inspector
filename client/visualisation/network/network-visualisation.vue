<template>
  <v-row style="height: 100%">
    <v-col md="9">
      <d3-chart-network
        :nodes="nodes"
        :edges="edges"
        :highlight="highlight"
        :labels="labels"
        :nodes-properties="nodesProperties"
      />
    </v-col>
    <v-col
      md="3"
      style="overflow-y: scroll"
    >
      <div class="toolbar">
        Paths are ready: {{ pathsAreAvailable }}
        <v-list>
          <v-list-item
            v-for="dataset in datasets"
            :key="dataset.url"
          >
            <v-list-item-content>
              <v-list-item-title>
                <a
                  :href="dataset.url"
                  target="_blank"
                >{{ dataset.metadata.title }}</a>
                <v-btn
                  fab
                  dark
                  color="red"
                  class="remove-dataset-button"
                  elevation="0"
                  @click="onDeleteDataset(dataset)"
                >
                  <v-icon dark>
                    mdi-minus
                  </v-icon>
                </v-btn>
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ dataset.collection }}
                <div v-if="dataset.loaded && mappings[dataset.url]">
                  <v-switch
                    v-model="mappings[dataset.url].showTitle"
                    :label="switchTitle(mappings[dataset.url])"
                    :color="mappings[dataset.url].color"
                    class="visibility-switch"
                    @change="onVisibilityChange(mappings[dataset.url])"
                  />
                  <v-switch
                    v-model="mappings[dataset.url].showDescription"
                    :label="switchDescription(mappings[dataset.url])"
                    :color="mappings[dataset.url].color"
                    class="visibility-switch"
                    @change="onVisibilityChange(mappings[dataset.url])"
                  />
                  <v-switch
                    v-model="mappings[dataset.url].showKeywords"
                    :label="switchKeywords(mappings[dataset.url])"
                    :color="mappings[dataset.url].color"
                    class="visibility-switch"
                    @change="onVisibilityChange(mappings[dataset.url])"
                  />
                </div>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-btn
            v-show="datasets.length < 2"
            fab
            dark
            small
            color="green"
            @click="onAddDataset"
          >
            <v-icon dark>
              mdi-plus
            </v-icon>
          </v-btn>
        </v-list>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import Chart from "./d3-chart-network.vue";
import { createHighlightsFilter } from "../visualisation-service.ts";

export default {
  "name": "network-visualisation",
  "components": {
    "d3-chart-network": Chart,
  },
  "props": {
    "datasets": { "type": Array, "required": true },
    "nodes": { "type": Array, "required": true },
    "edges": { "type": Array, "required": true },
    "labels": { "type": Object, "required": true },
    "nodesProperties": { "type": Object, "required": true },
    "highlightOptions": { "type": Object, "required": true },
    "paths": { "type": Array },
    "pathsAreAvailable": { "type": Boolean, "required": true },
  },
  "data": () => ({
    "mappings": {},
    "highlight": {}, // [color] = Set(ids)
  }),
  "mounted": function () {
    this.updateMappings(this.datasets);
    this.highlight = createHighlights(
      this.mappings, this.highlightOptions, this.paths
    );
  },
  "watch": {
    "datasets": function (datasets) {
      // We need to keep this.mappings list in sync with datasets.
      this.updateMappings(datasets);
      this.highlight = createHighlights(
        this.mappings, this.highlightOptions, this.paths
      );
    },
    "paths": function () {
      this.highlight = createHighlights(
        this.mappings, this.highlightOptions, this.paths
      );
    },
    "highlightOptions": function () {
      this.highlight = createHighlights(
        this.mappings, this.highlightOptions, this.paths
      );
    },
  },
  "methods": {
    "updateMappings": function (datasets) {
      const colors = new Set(generateNewColor(datasets.length));
      const newMappings = {};
      // Update existing.
      datasets.forEach((dataset) => {
        const prevMapping = this.mappings[dataset.url];
        if (prevMapping === undefined) {
          return;
        }
        const mapping = updateMappingForDataset(
          dataset, this.mappings[dataset.url]
        );
        colors.delete(mapping.color);
        newMappings[dataset.url] = mapping;
      });
      const unusedColors = [...colors];
      // Add new.
      datasets.forEach((dataset) => {
        if (newMappings[dataset.url] !== undefined) {
          return;
        }
        newMappings[dataset.url] = createNewMappingFromDataset(
          dataset, unusedColors.pop()
        );
      });
      this.mappings = newMappings;
    },
    "switchTitle": function (mapping) {
      return `Show title mapping (${mapping.title.length})`;
    },
    "switchDescription": function (mapping) {
      return `Show description mapping (${mapping.description.length})`;
    },
    "switchKeywords": function (mapping) {
      return `Show keyword mapping (${mapping.keywords.length})`;
    },
    //
    "onDeleteDataset": function (dataset) {
      this.$emit("remove-dataset", dataset);
    },
    "onAddDataset": function () {
      this.$emit("add-dataset");
    },
    // eslint-disable-next-line no-unused-vars
    "onVisibilityChange": function (mapping) {
      // TODO Only toggle those from mapping.
      this.highlight = createHighlights(
        this.mappings, this.highlightOptions, this.paths
      );
    },
  },
};

function updateMappingForDataset(dataset, mapping) {
  if (mapping.loaded === dataset.loaded) {
    return mapping;
  }
  if (!dataset.loaded) {
    return mapping;
  }
  return {
    ...mapping,
    ...collectMappingsFromDataset(dataset),
  };
}

function collectMappingsFromDataset(dataset) {
  const result = {};
  for (const mapping of dataset.mappings) {
    result[mapping.metadata.from] = Object.freeze(
      mapping.data.map((item) => item.id)
    );
  }
  return result;
}

function createNewMappingFromDataset(dataset, color) {
  let mapping = {
    "url": dataset.url,
    "showTitle": true,
    "showDescription": true,
    "showKeywords": true,
    "loaded": dataset.loaded,
    "title": [],
    "description": [],
    "keywords": [],
    "color": color,
  };
  if (dataset.loaded) {
    mapping = {
      ...mapping,
      ...collectMappingsFromDataset(dataset),
    };
  }
  return mapping;
}

function generateNewColor(count) {
  const result = [];
  for (let index = 0; index < count; index += 1) {
    // eslint-disable-next-line no-mixed-operators
    const hls = (index * (360 / count) % 360);
    result.push(`hsl(${hls},100%,70%)`);
  }
  return result;
}

/**
 * Create nw highlight object.
 */
function createHighlights(mappings, options, paths) {
  const result = {};
  const filter = createHighlightsFilter(paths, options);
  for (const mapping of Object.values(mappings)) {
    result[mapping.color] = filter([
      ...(mapping.showTitle ? mapping.title : []),
      ...(mapping.showDescription ? mapping.description : []),
      ...(mapping.showKeywords ? mapping.keywords : []),
    ]);
  }
  return result;
}


</script>

<style scoped>
  .visibility-switch {
    margin-left: 1rem;
    margin-top: 0;
    margin-bottom: -1rem; /* Hyde space for v-message. */
  }
  .remove-dataset-button {
    float: right;
    width: 1.5rem;
    height: 1.5rem;
  }
</style>
