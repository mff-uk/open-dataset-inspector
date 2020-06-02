<template>
  <v-dialog
    v-model="visible"
    max-width="40rem"
    persistent
  >
    <v-card>
      <v-card-title>
        <span class="headline">
          Highlight configuration
        </span>
      </v-card-title>
      <v-card-text>
        <v-switch
          v-model="local.usedInPaths"
          label="Show only nodes used in paths if paths are available"
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
  "name": "highlight-options-dialog",
  "props": {
    "visible": { "type": Boolean, "required": true },
    "options": { "type": Object, "required": true },
  },
  "data": () => ({
    "local": {
      "usedInPaths": undefined,
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
      this.$emit("accept", this.local);
    },
  },
};
</script>
