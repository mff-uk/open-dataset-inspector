<template>
  <v-dialog
    v-model="value"
    max-width="40rem"
  >
    <v-card>
      <v-card-title>
        <span class="headline">
          Select dataset
        </span>
      </v-card-title>
      <v-card-text>
        <v-combobox
          v-model="collection"
          :items="collections"
          label="Collection"
        />
        <v-text-field
          v-model="url"
          label="URL"
        />
      </v-card-text>
      <v-card-actions>
        <div class="flex-grow-1" />
        <v-btn
          text
          @click="onClose"
        >
          Close
        </v-btn>
        <v-btn
          text
          color="primary"
          @click="onAdd"
        >
          Add
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  "name": "add-dataset-dialog",
  "props": {
    "value": { "type": Boolean, "required": true },
  },
  "data": () => ({
    "collection": "v1",
    "collections": [
      "v1",
    ],
    "url": "https://data.gov.cz/zdroj/datové-sady/MDopravy/225009945",
  }),
  "methods": {
    "onClose": function () {
      this.$emit("input", false);
    },
    "onAdd": function () {
      this.$emit("input", false);
      this.$emit("add-dataset", {
        "collection": this.collection,
        "dataset": this.url,
      });
    },
  },
};
</script>
