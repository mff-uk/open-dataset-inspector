<template>
  <div>
    <strong>{{ label }}</strong>
    <v-expansion-panels
      multiple
    >
      <v-expansion-panel
        v-for="(dataset, index) in datasets"
        :key="index"
      >
        <v-expansion-panel-header>
          {{ dataset.title }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <strong>Description:</strong> {{ dataset.description }} <br>
          <br>
          <strong>Keywords:</strong>
          <v-chip
            v-for="keyword in dataset.keywords"
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
  },
};
</script>
