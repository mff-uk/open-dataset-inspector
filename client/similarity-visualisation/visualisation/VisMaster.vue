<template>
  <v-container>
    <v-row>
      <vis-container
        v-bind:leftDataset="leftDataset"
        v-bind:rightDataset="rightDataset"
        v-bind:activeView="activeView"
      >
      </vis-container>
    </v-row>
      <layout
        v-bind:pathsDataset="paths"
        v-bind:leftDataset="leftDataset"
        v-bind:rightDataset="rightDataset"
        v-bind:activeView="activeView"
      >
    </layout>
    <v-row>
    </v-row>
    <custom-menu
      @leftDatasetChanged="leftDatasetChanged"
      @rightDatasetChanged="rightDatasetChanged"
      @pathsDatasetChanged="pathsDatasetChanged"
      @setTreeView="setTreeView"
      @setCircleView="setCircleView"
    ></custom-menu>
  </v-container>
</template>

<script lang='ts'>
import Vue from 'vue'
import Layout from './Layout.vue'
import VisContainer from './VisContainer.vue'
import axios from 'axios'
import CustomMenu from './CustomMenu.vue'

export default Vue.extend({
  name: 'VisMaster',
  components: {
    CustomMenu,
    Layout,
    VisContainer
  },
  data: () => ({
    error: Error(),
    leftDataset: undefined,
    rightDataset: undefined,
    paths: undefined,
    activeView: 1
  }),
  methods: {
    leftDatasetChanged: function () {
      this.$emit('leftDatasetChanged')
    },
    rightDatasetChanged: function () {
      this.$emit('rightDatasetChanged')
    },
    pathsDatasetChanged: function () {
      this.$emit('pathsDatasetChanged')
    },
    setTreeView: function () {
      this.activeView = 2
    },
    setCircleView: function () {
      this.activeView = 1
    }
  }
})
</script>
