<template>
  <v-container
    class="text-center"
    fluid
  >
    <v-container>
      <v-row>
        <v-btn
          :disabled="index === 0"
          text
          @click="onPrevious"
        >
          Previous
        </v-btn>
        <v-btn
          :disabled="index + 1 >= collection.length"
          text
          @click="onNext"
        >
          Previous
        </v-btn>
        <v-spacer />
        {{ index + 1 }} / {{ collection.length }}
      </v-row>
    </v-container>
    <v-container>
      <h2>Datasets</h2>
      <app-dataset
        :iri="active.datasets[0]"
        :languages="languages"
      />
      <br/>
      <app-dataset
        :iri="active.datasets[1]"
        :languages="languages"
      />
    </v-container>
    <v-container fluid>
      <h2>Explanations</h2>
      <br />
      <div
        v-for="method in active.methods"
        :key="method.id"
      >
        <h3 style="text-align: left">
          {{ method["label"] }}
        </h3>
        <div class="explanation-container">
          <div v-if="active.explanation[method.id] === undefined">
            Loading ...
          </div>
          <app-explain-transitive
            v-else-if="method.explanation === 'transitive-similarity'"
            :explanation="active.explanation[method.id]"
          />
          <div v-else>
            Unknown similarity data ...
          </div>
        </div>
      </div>
    </v-container>
  </v-container>
</template>

<script>
import DatasetDetail from "./dataset-detail.vue";
import ExplainTransitive from "./explain-transitive.vue";

import { fetchSimilarityMethods } from "../app-service/similarity-api.ts";
import { fetchExplanation } from "../app-service/explanation-api.ts";

export default {
  "name": "similarity-explanation",
  "components": {
    "app-dataset": DatasetDetail,
    "app-explain-transitive": ExplainTransitive,
  },
  "data": () => ({
    "collection": [],
    "index": 0,
    // Reference to a collection member.
    "active": {
      "datasets": [],
      "methods": [],
      "explanation": {},
      "shouldLoad": false,
    },
    "languages": ["en", "cs"],
    "methods": {},
  }),
  "mounted": async function () {
    this.methods = await fetchSimilarityMethods();
    //
    const datasets = asArray(this.$route.query.dataset || []);
    let methods = asArray(this.$route.query.method || []);
    if (methods.length === 0) {
      methods = Object.keys(this.methods);
    }
    if (datasets.length === 2) {
      this.collection.push({
        "datasets": datasets,
        "methods": methods.map((name) => this.methods[name]),
        "explanation": {},
        "shouldLoad": true,
      });
    }
    this.active = this.collection[this.index];
    await this.fetchActive();
  },
  "methods": {
    "onPrevious": function () {
      this.index -= 1;
      this.active = this.collection[this.index];
      this.fetchActive();
    },
    "onNext": function () {
      this.index += 1;
      this.active = this.collection[this.index];
      this.fetchActive();
    },
    "fetchActive": async function () {
      // Capture the data as we are async.
      const capture = this.active;
      if (!capture.shouldLoad) {
        return;
      }
      capture.shouldLoad = false;
      const left = capture.datasets[0];
      const right = capture.datasets[1];
      for await (const method of capture.methods) {
        if (capture.explanation[method.id] !== undefined) {
          continue;
        }
        const response = await fetchExplanation(method.id, left, right);
        capture.explanation = {
          ...capture.explanation,
          [method.id]: response.explanation,
        };
      }
      console.log("Fetch for", capture);
    },
  },
};

function asArray(value) {
  return Array.isArray(value) ? value : [value];
}

</script>

<style scoped>
.explanation-container {
  margin: 2rem;
}
</style>
