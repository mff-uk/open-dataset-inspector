<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn
        v-bind:content="`Add paths file`"
        v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
        fab
        dark
        small
        v-on="on"
        color="indigo"
      >
        <v-icon>mdi-set-center</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Add paths</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="8" md="12">
              <v-text-field v-model="pathsUrl" label="URL" hint="Url of paths"></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
        <v-btn color="blue darken-1" text @click="changePaths">Add</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'AddPathsDialog',

  data: () => ({
    selectedMappingItems: [],
    pathsUrl: 'paths-shortest.json',
    dialog: false,
    display: true
  }),
  computed: {
  },
  methods: {
    changePaths: function () {
      this.dialog = false
      this.$emit('pathsDatasetChanged', this.pathsUrl)
    }
  }
})
</script>
