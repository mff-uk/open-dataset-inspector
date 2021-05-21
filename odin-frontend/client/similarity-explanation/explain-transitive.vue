<template>
  <div>
    <h4 style="text-align: left">
      Metadata
    </h4>
    <dl class="row">
      <template v-for="(data, index) in metadata">
        <dt
          :key="index + '-label'"
          class="col-sm-3"
        >
          {{ data.label }}
        </dt>
        <dd
          :key="index + '-value'"
          class="col-sm-9"
        >
          {{ data.value }}
        </dd>
      </template>
    </dl>
    <div v-show="paths.length > 0">
      <h4 style="text-align: left">
        Connecting datasets
      </h4>
      <app-dataset
        v-for="iri in paths"
        :key="iri"
        :iri="iri"
        class="path-dataset-detail"
      />
    </div>
  </div>
</template>
<script>
import DatasetDetail from "./dataset-detail.vue";

export default {
  "name": "similarity-explanation-explain-transitive",
  "components": {
    "app-dataset": DatasetDetail,
  },
  "props": {
    "explanation": { "type": Array, "required": true },
  },
  "computed": {
    // We convert the data into a metadata table.
    "metadata": function () {
      const explanation = this.explanation[0];
      return [
        {
          "label": "Type",
          "value": explanation.middle.length > 0
            ? "Transitive" : "Non-Transitive",
        }, {
          "label": "Distance",
          "value": explanation.dist,
        }, {
          "label": "Paths found",
          "value": explanation.middle.length,
        }, {
          "label": "Number of before",
          "value": explanation.lowerBound,
        }, {
          "label": "Number of equal",
          "value": explanation.upperBound - explanation.lowerBound,
        },
      ];
    },
    "paths": function () {
      const explanation = this.explanation[0];
      if (explanation === undefined) {
        return [];
      }
      return explanation.middle || [];
    },
  },
};
</script>

<style scoped>
.path-dataset-detail {
  margin: 1rem;
}
</style>
