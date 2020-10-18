<template>
  <div>
    <v-row>
      <vis-container
        v-bind:leftDataset="leftDataset"
        v-bind:rightDataset="rightDataset"
        v-bind:activeView="activeView"
        v-bind:labels="labels"
      />
    </v-row>
    <layout
      v-bind:pathsDataset="paths"
      v-bind:leftDataset="leftDataset"
      v-bind:rightDataset="rightDataset"
      v-bind:labels="labels"
      v-bind:activeView="activeView"
    />
  </div>
</template>

<script>
import Layout from './visualisation/Layout.vue'
import VisContainer from './visualisation/VisContainer.vue'

export default {
  "name": "similarity-visualisation",
  "components": {
    "layout" : Layout,
    "vis-container": VisContainer,
  },
  "props": {
    "leftDataset": Object,
    "rightDataset": Object,
    "paths": Array,
    "activeView": Number,
    "labels": Object
  }
}
</script>