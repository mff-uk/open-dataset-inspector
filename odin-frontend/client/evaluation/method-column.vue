<template>
  <div class="method">
    <div class="header">
      <v-text-field
        :value="Number(rating) + 1"
        :rules="[rules.required, rules.number]"
        label="Order"
        @input="onChangeRating"
      >
        <template v-slot:append-outer>
          <v-btn
            icon
            @click="onCopyRating"
          >
            <v-icon>mdi-arrow-expand-right</v-icon>
          </v-btn>
        </template>
      </v-text-field>
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
          :languages="languages"
        />
      </div>
    </div>
  </div>
</template>

<script>
import MethodColumnDataset from "../app-components/dataset-card.vue";
import { required, decimal } from "./validators.ts";

export default {
  "name": "method-column",
  "components": {
    "method-dataset": MethodColumnDataset,
  },
  "props": {
    "method": { "type": Object, "required": true },
    "datasets": { "type": Object, "required": true },
    "rating": { "type": String, "required": true },
    "highlights": { "type": Object, "required": true },
    "languages": { "type": Array, "required": true },
  },
  "data": () => ({
    "rules": {
      "required": (value) => required(value) || "Required.",
      "number":
        (value) => decimal(value) || "Must be a positive decimal number",
    },
  }),
  "methods": {
    "onChangeRating": function (value) {
      if (!decimal(value)) {
        return;
      }
      this.$emit("change-rating", Number(value) - 1);
    },
    "onCopyRating": function () {
      this.$emit("copy-rating", this.rating);
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
</style>
