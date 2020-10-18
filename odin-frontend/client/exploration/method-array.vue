<template>
  <div>
    <strong>Similar datasets:</strong>
    <v-row>
      <v-col
        v-for="method in methods"
        :key="method.id"
        cols="12"
        :md="columnSize.md"
      >
        <method-column
          :method="method"
          :datasets="datasets"
          :highlights="highlights"
          :expected="expected[method.id]"
          @load-more="onLoadMore"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import MethodColumn from "./method-column.vue";

export default {
  "name": "method-array",
  "components": {
    "method-column": MethodColumn,
    "draggable": draggable,
  },
  "props": {
    "datasets": { "type": Object, "required": true },
    "methods": { "type": Array, "required": true },
    "highlights": { "type": Object, "required": true },
    "expected": { "type": Object, "required": true },
  },
  "computed": {
    "columnSize": function () {
      return {
        "md": Math.max(3, 12 / this.methods.length),
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
