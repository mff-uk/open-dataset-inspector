<template>
  <v-dialog
    v-model="visible"
    max-width="40rem"
    persistent
  >
    <v-card>
      <v-card-title>
        <span class="headline">
          Mapping filter configuration
        </span>
      </v-card-title>
      <v-card-text>
        <v-switch
          v-model="local.directlyMapped"
          label="Keep only directly mapped"
        />
        <v-textarea
          v-model="local.userFilterFunction"
          label="Filter function"
          hint="Hint: (mapping) => mapping.metadata.directly_mapped"
        ></v-textarea>
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
  "name": "mapping-options-dialog",
  "props": {
    "visible": { "type": Boolean, "required": true },
    "options": { "type": Object, "required": true },
  },
  "data": () => ({
    "local": {
      "directlyMapped": undefined,
      "userFilterFunction": undefined,
    },
  }),
  "watch": {
    "visible": function (newValue) {
      if (newValue) {
        this.local = { ...this.options };
      }
    },
  },
  "methods": {
    "onClose": function () {
      this.$emit("reject", false);
    },
    "onConfirm": function () {
      let userFunction;
      try {
        // eslint-disable-next-line no-eval
        userFunction = eval(this.local.userFilterFunction);
      } catch (error) {
        alert(`Invalid user function: ${error}`);
        return;
      }
      this.local.compiledUserFilterFunction = userFunction;
      this.$emit("accept", this.local);
    },
  },
};
</script>
