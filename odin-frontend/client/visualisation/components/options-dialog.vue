<template>
  <v-dialog
    v-model="visible"
    max-width="40rem"
    persistent
  >
    <v-card>
      <v-card-title>
        <span class="headline">
          Configuration
        </span>
      </v-card-title>
      <v-card-text>
        <v-tabs
          v-model="activeTab"
          :grow="true"
        >
          <v-tab>
            Highlight
          </v-tab>
          <v-tab>
            Mapping
          </v-tab>
          <v-tab>
            Similarity
          </v-tab>
          <v-tab-item>
            <br/>
            <v-switch
              v-model="localHighlight.usedInPaths"
              label="Show only nodes used in paths if paths are available"
            />
          </v-tab-item>
          <v-tab-item>
            <br/>
            <v-switch
              v-model="localMapping.directlyMapped"
              label="Keep only directly mapped"
            />
            <v-textarea
              v-model="localMapping.userFilterFunction"
              label="Filter function"
              hint="Hint: (mapping) => mapping.metadata.directly_mapped"
            />
          </v-tab-item>
          <v-tab-item>
            <br/>
            <v-alert
              v-show="datasetCount !== 2"
              outlined
              type="error"
            >
              Similarity can be computed only if exactly two
              datasets are loaded.
            </v-alert>
            <v-switch
              v-model="localSimilarity.autoFetch"
              label="Fetch automatically on dataset change"
            />
            <v-combobox
              v-model="localSimilarity.method"
              :items="methods"
              item-text="label"
              item-value="value"
              label="Path calculation method"
            />
            <v-text-field
              v-model="localSimilarity.distance"
              :rules="distanceRules"
              label="Limit maximum path length"
            />
          </v-tab-item>
        </v-tabs>
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
          text
          color="primary"
          @click="onConfirm"
        >
          Accept
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  "name": "options-dialog",
  "props": {
    "visible": { "type": Boolean, "required": true },
    "highlight": { "type": Object, "required": true },
    "mapping": { "type": Object, "required": true },
    "similarity": { "type": Object, "required": true },
    "datasetCount": { "type": Number, "required": true },
  },
  "data": () => ({
    "activeTab": 0,
    "localHighlight": {
      "usedInPaths": undefined,
    },
    "localMapping": {
      "directlyMapped": undefined,
      "userFilterFunction": undefined,
    },
    "localSimilarity": {
      "method": undefined,
      "distance": undefined,
      "autoFetch": undefined,
    },
    "methods": [
      {
        "label": "Shorted paths",
        "value": "closest",
      }, {
        "label": "All paths",
        "value": "distance",
      },
    ],
  }),
  "watch": {
    "visible": function (newValue) {
      if (newValue === false) {
        return;
      }
      this.localHighlight = { ...this.highlight };
      this.localMapping = { ...this.mapping };
      this.localSimilarity = {
        ...this.similarity,
      };
      for (const method of this.methods) {
        if (method.value === this.similarity.method) {
          this.localSimilarity.method = method;
        }
      }
    },
  },
  "computed": {
    "distanceRules": function () {
      return [isNotNegativeInteger];
    },
    "canSubmit": function () {
      return isNotNegativeInteger(this.distance);
    },
  },
  "methods": {
    "setTab": function (value) {
      this.activeTab = value;
    },
    "onClose": function () {
      this.$emit("reject", false);
    },
    "onConfirm": function () {
      let userFunction;
      try {
        // eslint-disable-next-line no-eval
        userFunction = eval(this.localMapping.userFilterFunction);
      } catch (error) {
        alert(`Invalid user function: ${error}`);
        return;
      }
      this.localMapping.compiledUserFilterFunction = userFunction;
      //
      this.$emit("accept", {
        "highlight": this.localHighlight,
        "mapping": this.localMapping,
        "similarity": {
          "method": this.localSimilarity.method.value,
          "distance": Number.parseInt(this.localSimilarity.distance, 10),
          "autoFetch": this.localSimilarity.autoFetch,
        },
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
