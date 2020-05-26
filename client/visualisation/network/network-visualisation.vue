<template>
  <v-row style="height: 100%">
    <v-col md="9">
      <d3-chart-network
        :nodes="nodes"
        :edges="edges"
        :highlight="highlight"
        :labels="labels"
      />
    </v-col>
    <v-col
      md="3"
      style="overflow-y: scroll"
    >
      <div class="toolbar">
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
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ dataset.collection }}
                <div v-if="dataset.loaded">
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
        </v-list>
        <div style="bottom: 1rem; right: 1rem; position: absolute;">
          <v-btn
            fab
            dark
            class="mx-2"
            color="green"
            @click="onAddDataset"
          >
            <v-icon dark>
              mdi-plus
            </v-icon>
          </v-btn>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import Chart from "./d3-chart-network.vue";

export default {
  "name": "network-visualisation",
  "components": {
    [Chart.name]: Chart,
  },
  "props": {
    "datasets": { "type": Array, "required": true },
    "nodes": { "type": Array, "required": true },
    "edges": { "type": Array, "required": true },
    "labels": { "type": Object, "required": true },
  },
  "data": () => ({
    "mappings": {},
    "highlight": {}, // [color] = Set(ids)
  }),
  "watch": {
    "datasets": function (newDatasets) {
      // We need to keep this.mappings list in sync with datasets.
      //
      const colors = new Set(generateNewColor(newDatasets.length));
      const newMappings = {};
      // Update existing.
      newDatasets.forEach((dataset) => {
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
      newDatasets.forEach((dataset) => {
        if (newMappings[dataset.url] !== undefined) {
          return;
        }
        newMappings[dataset.url] = createNewMappingFromDataset(
          dataset, unusedColors.pop()
        );
      });
      this.mappings = newMappings;
      this.highlight = createHighlight(Object.values(this.mappings));
    },
  },
  "methods": {
    "switchTitle": function (mapping) {
      return `Show title mapping (${mapping.title.length})`;
    },
    "switchDescription": function (mapping) {
      return `Show description mapping (${mapping.description.length})`;
    },
    "switchKeywords": function (mapping) {
      return `Show keyword mapping (${mapping.keywords.length})`;
    },
    "onAddDataset": function () {
      this.$emit("add-dataset");
    },
    "onVisibilityChange": function (mapping) {
      this.highlight = updateHighlight(mapping, this.highlight);
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
function createHighlight(mappings) {
  const result = {};
  for (const mapping of mappings) {
    result[mapping.color] = new Set([
      ...(mapping.showTitle ? mapping.title : []),
      ...(mapping.showDescription ? mapping.description : []),
      ...(mapping.showKeywords ? mapping.keywords : []),
    ]);
  }
  return result;
}

/**
 * Update highlight selection only for given mapping.
 */
function updateHighlight(mapping, highlight) {
  const result = { ...highlight };
  result[mapping.color] = new Set([
    ...(mapping.showTitle ? mapping.title : []),
    ...(mapping.showDescription ? mapping.description : []),
    ...(mapping.showKeywords ? mapping.keywords : []),
  ]);
  return result;
}

</script>

<style scoped>
  .visibility-switch {
    margin-left: 1rem;
    margin-top: 0;
    margin-bottom: -1rem; /* Hyde space for v-message. */
  }
</style>
