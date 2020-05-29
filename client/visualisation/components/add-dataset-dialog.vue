<template>
  <v-dialog
    v-model="visible"
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
    "visible": { "type": Boolean, "required": true },
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
      this.$emit("reject", false);
    },
    "onAdd": function () {
      this.$emit("accept", {
        "collection": this.collection,
        "dataset": this.url,
      });
    },
  },
};
</script>
