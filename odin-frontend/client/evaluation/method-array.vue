<template>
  <div>
    <strong>Similar datasets:</strong>
    <draggable
      :value="methods"
      class="row method-array"
      @input="onChangeOrder"
    >
      <v-col
        v-for="(method, index) in methods"
        :key="method.id"
        xs="12"
        sm="6"
        :md="columnSize.md"
        :lg="columnSize.lg"
        :xl="columnSize.xl"
      >
        <method-column
          :method="method"
          :datasets="datasets"
          :rating="ratings[method.id]"
          :highlights="highlights"
          @change-rating="(value) => onChangeMethodRating(method, value)"
          @copy-rating="(value) => onCopyMethodRating(index, value)"
        />
      </v-col>
    </draggable>
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
    "ratings": { "type": Object, "required": true },
    "highlights": { "type": Object, "required": true },
  },
  "computed": {
    "columnSize": function () {
      return {
        "md": Math.ceil(Math.max(3, 12 / this.methods.length)),
        "lg": Math.ceil(Math.max(3, 12 / this.methods.length)),
        "xl": Math.floor(Math.max(2, 12 / this.methods.length)),
      };
    },
  },
  "methods": {
    "onChangeOrder": function (methods) {
      this.$emit("change-order", methods);
    },
    "onChangeMethodRating": function (method, value) {
      this.$emit("change-method-rating", {
        "method": method,
        "value": value,
      });
    },
    "onCopyMethodRating": function (index, value) {
      this.$emit("copy-rating", {
        "from": index,
        "value": value,
      });
    },
  },
};
</script>

<style scoped>
  @media only screen and (max-width: 960px) {
    .method-array {
      margin-right: 2rem
    }
  }
</style>
