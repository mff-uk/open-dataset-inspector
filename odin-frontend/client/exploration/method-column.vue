<template>
  <div class="method">
    <div class="header">
      {{ method.id }}
    </div>
    <div class="datasets">
      <div
        v-for="item in method.datasets"
        :key="item.iri"
      >
        <method-dataset
          :iri="item.iri"
          :dataset="datasets[item.iri]"
          :background-color="highlights[item.iri]"
          :score="item.score"
        />
      </div>
      <div
        v-for="item in expectedDatasets"
        :key="item.iri"
      >
        <div class="position">
          ... {{ item.positionMin }}
          <span v-if="item.positionMin !== item.positionMax">
            - {{ item.positionMax }}
          </span>
        </div>
        <method-dataset
          :iri="item.iri"
          :dataset="datasets[item.iri]"
          :score="item.score"
          :position="item.index"
        />
      </div>
    </div>
    <div class="footer">
      Visible {{ Object.keys(method.datasets).length }}
      With same score
      {{ method.numSameScoreAsLast }} / {{ method.numDatasets }}
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
import MethodColumnDataset from "../evaluation/method-column-dataset.vue";

export default {
  "name": "method-column",
  "components": {
    "method-dataset": MethodColumnDataset,
  },
  "props": {
    "method": { "type": Object, "required": true },
    "datasets": { "type": Object, "required": true },
    "highlights": { "type": Object, "required": true },
    "expected": { "type": Array, "required": true },
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
