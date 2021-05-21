<template>
  <div v-show="datasets.length > 0">
    <strong>{{ label }}</strong>
    <v-expansion-panels
      multiple
    >
      <v-expansion-panel
        v-for="(dataset, index) in datasets"
        :key="index"
      >
        <v-expansion-panel-header>
          {{ select(dataset, "title", "") }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <strong>Description:</strong>
          {{ select(dataset, "description", "") }}
          <br>
          <br>
          <strong>Keywords:</strong>
          <v-chip
            v-for="keyword in select(dataset, 'keywords', [])"
            :key="keyword"
            x-small
            style="margin-right: 0.5rem"
          >
            {{ keyword }}
          </v-chip>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
export default {
  "name": "query-dataset-detail",
  "props": {
    "label": { "type": String, "requried": true },
    "datasets": { "type": Array, "requried": true },
    "languages": { "type": Array, "requried": true },
  },
  "methods": {
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
