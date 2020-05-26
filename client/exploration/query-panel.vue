<template>
  <v-expansion-panels multiple>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Group details
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        {{ description }}
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Query
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-text-field
          v-model="group"
          label="Method group ID"
        />
        <v-select
          v-model="fusion"
          :items="fusionMethods"
          item-text="label"
          item-value="value"
          label="Fusion method"
        />
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
        <v-btn
          style="float:right;"
          @click="onSearch"
        >
          Search
        </v-btn>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  "name": "query-panel",
  "props": {
    "query": { "type": Object, "required": true },
    "description": { "type": String },
  },
  "data": () => ({
    "group": "",
    "dataset": "",
    "expected": "",
    "fusion": "max",
    "fusionMethods": [
      { "label": "Max-fusion", "value": "max" },
      { "label": "Min-fusion", "value": "min" },
    ],
  }),
  "watch": {
    "query": function (query) {
      this.group = query.group;
      this.dataset = query.dataset;
      this.expected = query.expected;
      this.fusion = query.fusion;
    },
  },
  "methods": {
    "onSearch": function () {
      this.$emit("search", {
        "group": this.group,
        "dataset": this.dataset,
        "expected": this.expected,
        "fusion": this.fusion,
      });
    },
  },
};
</script>
