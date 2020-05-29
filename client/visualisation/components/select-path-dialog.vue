<template>
  <v-dialog
    v-model="visible"
    max-width="40rem"
  >
    <v-card>
      <v-card-title>
        <span class="headline">
          Select path
        </span>
      </v-card-title>
      <v-card-text>
        <v-alert
          v-show="datasetCount !== 2"
          outlined
          type="error"
        >
          Paths can be computed only if exactly two datasets are loaded.
        </v-alert>
        <v-switch
          v-model="local.autoFetch"
          label="Fetch automatically on dataset change"
        />
        <v-combobox
          v-model="local.method"
          :items="methods"
          item-text="label"
          item-value="value"
          label="Path calculation method"
        />
        <v-text-field
          v-model="local.distance"
          :rules="distanceRules"
          label="Limit maximum path length"
        />
      </v-card-text>
      <v-card-actions>
        <div class="flex-grow-1" />
        <v-btn
          text
          @click="onClose"
        >
          Discard changes
        </v-btn>
        <v-btn
          :disabled="!canSubmit"
          text
          color="primary"
          @click="onSubmit"
        >
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  "name": "select-path-dialog",
  "props": {
    "visible": { "type": Boolean, "required": true },
    "options": { "type": Object, "required": true },
    "datasetCount": { "type": Number, "required": true },
  },
  "data": () => ({
    "methods": [
      {
        "label": "Shorted paths for all pairs",
        "value": "closest",
      }, {
        "label": "All",
        "value": "distance",
      },
    ],
    "local": {
      "method": undefined,
      "distance": undefined,
      "autoFetch": undefined,
    },
  }),
  "watch": {
    "visible": function (newValue) {
      if (newValue) {
        this.local = { ...this.options };
      }
    },
  },
  "computed": {
    "distanceRules": function () {
      return [isNotNegativeInteger];
    },
    "canSubmit": function () {
      return this.datasetCount === 2 && isNotNegativeInteger(this.distance);
    },
  },
  "methods": {
    "onClose": function () {
      this.$emit("reject", false);
    },
    "onSubmit": function () {
      this.$emit("accept", {
        "method": this.local.value,
        // Distance 2 is for nodes next to each other.
        "distance": Number.parseInt(this.local.distance, 10) + 2,
        "autoFetch": this.local.autoFetch,
      });
    },
  },
};

function isNotNegativeInteger(value) {
  return isNumber(value) && isNotNegative(value);
}

function isNumber(value) {
  return Number.isInteger(Number(value))
    || "The value must be an integer number";
}

function isNotNegative(value) {
  return value >= 0 || "The value must be greater than zero";
}

</script>
