<template>
  <div>
    <strong>Similar datasets:</strong>
    <v-row>
      <v-col
        v-for="methodId in Object.keys(similar)"
        :key="methodId"
        cols="12"
        :md="columnSize.md"
      >
        <method-column
          :query="query"
          :method="methods[methodId]"
          :datasets="datasets"
          :similar="similar[methodId]"
          :expected="expected[methodId]"
          :languages="languages"
          @load-more="onLoadMore"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import MethodColumn from "./method-column.vue";

export default {
  "name": "method-array",
  "components": {
    "method-column": MethodColumn,
  },
  "props": {
    "query": { "type": Array },
    "datasets": { "type": Object, "required": true },
    "methods": { "type": Object, "required": true },
    "similar": { "type": Object, "required": true },
    "expected": { "type": Object, "required": true },
    "languages": { "type": Array, "requried": true },
  },
  "computed": {
    "columnSize": function () {
      return {
        "md": Math.max(3, 12 / Object.keys(this.similar).length),
      };
    },
  },
  "methods": {
    "onLoadMore": function (method) {
      this.$emit("load-more", method);
    },
  },
};
</script>
