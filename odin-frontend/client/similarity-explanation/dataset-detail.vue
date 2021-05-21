<template>
  <div v-if="iri !== undefined">
    <v-card v-if="!loading">
      <v-card-title class="headline">
        {{ title }}
        <a
          style="text-decoration: none; margin-left: 1rem"
          :href="iri"
          rel="nofollow noopener noreferrer"
          target="_blank"
        >
          <v-icon
            style="color: #1976d2"
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-card-title>
      <v-card-text style="text-align: left">
        <div>
          <v-chip
            v-for="keyword in keywords"
            :key="keyword"
            x-small
            style="margin-right: 0.5rem"
          >
            {{ keyword }}
          </v-chip>
        </div>
        {{ description }}
      </v-card-text>
    </v-card>
    <v-card v-else>
      <v-card-title>
        Loading ...
      </v-card-title>
      <v-card-text>
        {{ this.iri }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { fetchDataset } from "../app-service/dataset-api.ts";

export default {
  "name": "similarity-explanation-dataset-detail",
  "props": {
    "iri": { "type": String },
    "languages": { "type": Array, "required": true },
  },
  "data": () => ({
    "title": "",
    "description": "",
    "keywords": [],
    "loading": false,
  }),
  "mounted": function () {
    this.fetchData();
  },
  "watch": {
    "iri": function () {
      this.fetchData();
    },
  },
  "methods": {
    "fetchData": async function () {
      const iri = this.iri;
      if (iri === undefined) {
        return;
      }
      this.loading = true;
      const dataset = await fetchDataset(iri);
      if (iri !== dataset.iri) {
        // Dataset may have changed during loading.
        return;
      }
      this.title = this.select(dataset, "title", iri);
      this.description = this.select(dataset, "description", "");
      this.keywords = this.select(dataset, "keywords", []);
      this.loading = false;
    },
    "select": function (dataset, property, defaultValue) {
      const values = dataset[property];
      for (const language of this.languages) {
        if (values[language] === undefined) {
          continue;
        }
        return values[language];
      }
      return defaultValue;
    },
  },
};
</script>
