<template>
  <div
    :style="'background-color:' + backgroundColor"
    class="dataset"
  >
    {{ score !== undefined ? "[" + score+ "]": "" }} {{ title }}
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          icon
          v-on="on"
          @click="showDescriptionDialog = true"
        >
          <v-icon small>
            mdi-help-circle-outline
          </v-icon>
        </v-btn>
      </template>
      <span> {{ description }} </span>
    </v-tooltip>
    <v-dialog v-model="showDescriptionDialog">
      <v-card>
        <v-card-title class="headline">
          Dataset description
        </v-card-title>
        <v-card-text>
          {{ description }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            text
            @click="showDescriptionDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <a
      style="text-decoration: none"
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
    <v-btn
      v-if="explainable"
      :to="{
        'name':'similarity-explanation',
        'query': {'dataset': [query, iri]}}"
      class="mx-2"
      text
      x-small
    >
      Explain
    </v-btn>
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
  </div>
</template>

<script>
// Detail of a single dataset.
export default {
  "name": "method-column-dataset",
  "props": {
    "query": { "type": String },
    "iri": { "type": String, "required": true },
    "score": { "type": Number },
    "dataset": { "type": Object },
    "backgroundColor": { "type": String },
    "languages": { "type": Array, "required": true },
    "explainable": { "type": Boolean, "default": false },
  },
  "data": () => ({
    "showDescriptionDialog": false,
  }),
  "computed": {
    "title": function () {
      if (this.dataset === undefined) {
        return this.iri;
      }
      for (const language of this.languages) {
        if (this.dataset.title[language]) {
          return this.dataset.title[language];
        }
      }
      return this.iri;
    },
    "keywords": function () {
      if (this.dataset === undefined) {
        return this.iri;
      }
      for (const language of this.languages) {
        if (this.dataset.keywords[language]) {
          return this.dataset.keywords[language];
        }
      }
      return [];
    },
    "description": function () {
      if (this.dataset === undefined) {
        return this.iri;
      }
      for (const language of this.languages) {
        if (this.dataset.description[language]) {
          return this.dataset.description[language];
        }
      }
      return "";
    },
  },
};
</script>

<style scoped>
  .dataset {
    background-color: white;
    margin: 0.25rem;
    padding: 0.5rem;
    border-radius: 0.25rem;
  }
</style>
