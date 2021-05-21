<template>
  <div class="method">
    <div class="header ma-2">
      {{ method.label }}
    </div>
    <div class="datasets">
      <div
        v-for="item in similar.datasets"
        :key="item.iri"
      >
        <method-dataset
          :query="query[0]"
          :iri="item.iri"
          :dataset="datasets[item.iri]"
          :score="item.score"
          :languages="languages"
          :explainable="method.explainable && query.length === 1"
        />
      </div>
      <div
        v-for="item in expected"
        :key="item.iri"
      >
        <div class="position">
          ... {{ item.positionMin }}
          <span v-if="item.positionMin !== item.positionMax">
            - {{ item.positionMax }}
          </span>
        </div>
        <method-dataset
          :query="query[0]"
          :iri="item.iri"
          :dataset="datasets[item.iri]"
          :score="item.score"
          :position="item.index"
          :languages="languages"
          :explainable="method.explainable && query.length === 1"
        />
      </div>
    </div>
    <div class="footer">
      Visible {{ Object.keys(similar.datasets).length }}
      With same score
      {{ similar.numberOfDatasetsWithSameScoreAsTheLast }}
      /
      {{ similar.numberOfDatasets }}
      <v-btn
        x-small
        style="float: right"
        @click="onLoadMore"
      >
        Show more
      </v-btn>
    </div>
  </div>
</template>

<script>
import MethodColumnDataset from "../app-components/dataset-card.vue";

export default {
  "name": "method-column",
  "components": {
    "method-dataset": MethodColumnDataset,
  },
  "props": {
    "query": { "type": Array },
    "method": { "type": Object, "required": true },
    "datasets": { "type": Object, "required": true },
    "similar": { "type": Object, "required": true },
    "expected": { "type": Array, "required": true },
    "languages": { "type": Array, "required": true },
  },
  "computed": {
    "expectedDatasets": function () {
      const visibleIris = new Set(this.method.datasets.map((item) => item.iri));
      return this.expected.filter((item) => !visibleIris.has(item.iri));
    },
  },
  "methods": {
    "onChangeRating": function (value) {
      this.$emit("change-rating", value);
    },
    "onLoadMore": function () {
      this.$emit("load-more", this.method);
    },
  },
};
</script>

<style scoped>
  .method {
    background-color: lightgray;
    padding: 0.1rem;
    border-radius: 0.5rem;
  }
  .header {
    margin: 0 1rem 0 1rem;
  }
  .datasets {
    margin: 0;
  }
  .footer {
    padding: 0.5rem;
  }
  .position {
    margin: 0 1rem 0 1rem;
    background-color: lightgray;
  }
</style>
