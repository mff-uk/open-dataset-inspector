<template>
  <v-card>
      <v-card-title>
        <span class="headline">Add dataset</span>
      </v-card-title>
      <p>dataset1.json and dataset2.json are available</p>
      <v-card-text>
        <v-container>
          <v-row>
            <v-combobox
              v-model="collection"
              :items="collectionItems"
              label="Collection"
            />
          </v-row>
          <v-row>
            <v-col cols="12" sm="8" md="12">
              <v-text-field v-model="datasetUrl" label="URL" hint="Url of dataset"></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialogClosed">Close</v-btn>
        <v-btn color="blue darken-1" text @click="datasetChanged">Add</v-btn>
      </v-card-actions>
    </v-card>
</template>

<script>
export default {
  name: 'AddDatasetForm',

  data: () => ({
    collectionItems:
      ['hierarchy.v1',
        'hierarchy.v2',
        'hierarchy.v3',
        'hierarchy.v3.reduced'
      ],
    collection: 'hierarchy.v1',
    selectedMappingItems: [],
    datasetUrl: ''
  }),
  methods: {
    datasetChanged: function () {
      this.dialog = false
      this.$emit('datasetChanged', this.datasetUrl, this.collection)
    },
    dialogClosed: function () {
      this.$emit('dialogClosed')
    }
  }
}
</script>

<style>

</style>
