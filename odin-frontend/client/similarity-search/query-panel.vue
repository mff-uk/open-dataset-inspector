<template>
  <v-expansion-panels multiple>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Methods
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-select
          v-model="selectedMethods"
          :items="methods"
          item-value="id"
          item-text="label"
          chips
          multiple
          deletable-chips
        />
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Query
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-textarea
          v-model="dataset"
          label="Query datasets"
          hint="Dataset IRI"
        />
        <v-textarea
          v-model="expected"
          label="expected datasets"
          hint="Dataset IRI"
        />
      </v-expansion-panel-content>
      <v-btn
        class="ma-4"
        @click="onSearch"
      >
        Search
      </v-btn>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import { queryParamsToText, textToArray } from "../utils.ts";

export default {
  "name": "query-panel",
  "props": {
    "query": { "type": Object, "required": true },
    "methods": { "type": Array },
  },
  "data": () => ({
    "dataset": "",
    "expected": "",
    "selectedMethods": [],
  }),
  "watch": {
    "query": function (query) {
      this.dataset = queryParamsToText(query.dataset);
      this.expected = queryParamsToText(query.expected);
      this.selectedMethods = query.method;
    },
  },
  "methods": {
    "onSearch": function () {
      this.$emit("search", {
        ...this.query,
        "dataset": textToArray(this.dataset),
        "expected": textToArray(this.expected),
        "method": this.selectedMethods,
      });
    },
  },
};
</script>
