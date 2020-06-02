<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <side-bar
          @mappingChoosed="mappingChoosed"
          @mappingChanged="mappingChanged"
          v-bind:mappingList="leftMappingTree"
          v-bind:sidebarPosition="left"
          v-bind:title="leftInfo.title"
          v-bind:collection="leftInfo.collection"
          v-bind:description="leftInfo.description"
          v-bind:url="leftInfo.url"
          v-bind:keywords="leftInfo.keywords"
        >
        </side-bar>
      </v-col>
      <v-col cols="8">
        <circle-visualisation
          v-bind:leftDataset="leftDataset"
          v-bind:rightDataset="rightDataset"
          v-bind:labels="labels"
          v-if="activeView === 1"
        ></circle-visualisation>
        <tree-visualisation
          v-bind:leftDataset="leftDataset"
          v-bind:rightDataset="rightDataset"
          v-bind:labels="labels"
          v-if="activeView === 2"
        ></tree-visualisation>
      </v-col>
      <v-col cols="2">
        <side-bar
          @mappingChoosed="mappingChoosed"
          @mappingChanged="mappingChanged"
          v-bind:mappingList="rightMappingTree"
          v-bind:sidebarPosition="right"
          :title="rightInfo.title"
          :collection="rightInfo.collection"
          :description="rightInfo.description"
          :url="rightInfo.url"
          :keywords="rightInfo.keywords"
        >
        </side-bar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapActions, mapMutations, mapGetters } from 'vuex'
import { Position, MappingNode, ROOT_ID, ROOT_LABEL, ComboboxItem } from '../models'
import { Actions, Mutations, Getters, STORE_NAME } from './Visualisation.store'
import { addMappingItemToArray, createNodes, createVisitedNode } from '../utils/nodesUtils'
import { createMapping, createLabels, createHierarchy } from '../utils/hierarchyUtils'
import SideBar from './Layout/SideBar.vue'
import CircleVisualisation from './CircleVisualisation/CircleVisualisation.vue'
import TreeVisualisation from './TreeVisualisation/TreeVisualisation.vue'

export default Vue.extend({
  name: 'VisContainer',
  components: {
    SideBar,
    CircleVisualisation,
    TreeVisualisation
  },
  props: ['rightDataset', 'leftDataset', 'activeView', 'labels'],
  data: () => ({
    left: Position.Left,
    right: Position.Right,
    leftMappingTree: Array<MappingNode>(),
    rightMappingTree: Array<MappingNode>(),
    leftInfo: {
      title: "",
      collection: "",
      description: "",
      url: "",
      keywords: [""]
    },
    rightInfo: {
      title: "",
      collection: "",
      description: "",
      url: "",
      keywords: [""]
    }
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      hierarchy: Getters.GET_HIERARCHY
    })
  },
  created () {
    if (this.leftDataset !== undefined) {
      const position = Position.Left
      const dataset = this.leftDataset
      this.updateMappingsCombobox(dataset, position)
      this.changeLeftMapping(Array<MappingNode>())
      this.leftInfo = {
        title: this.leftDataset.metadata.title,
        description: this.leftDataset.metadata.description,
        url: this.leftDataset.url,
        keywords: this.leftDataset.metadata.keywords,
        collection: this.leftDataset.collection
      }
    }
    if (this.rightDataset !== undefined) {
      const position = Position.Right
      const dataset = this.rightDataset
      this.updateMappingsCombobox(dataset, position)
      this.changeRightMapping(Array<MappingNode>()),
      this.rightInfo = {
        title: this.rightDataset.metadata.title,
        description: this.rightDataset.metadata.description,
        url: this.rightDataset.url,
        keywords: this.rightDataset.metadata.keywords,
        collection: this.rightDataset.collection
      }
    }
  },
  mounted () {
    if (this.leftDataset !== undefined) {
      this.initializeVisualisation()
      const position = Position.Left
      const dataset = this.leftDataset
      this.updateMappingsCombobox(dataset, position)
      this.changeLeftMapping(Array<MappingNode>())
      this.leftInfo = {
        title: this.leftDataset.metadata.title,
        description: this.leftDataset.metadata.description,
        url: this.leftDataset.url,
        keywords: this.leftDataset.metadata.keywords,
        collection: this.leftDataset.collection
      }
    }
    if (this.rightDataset !== undefined) {
      this.initializeVisualisation()
      const position = Position.Right
      const dataset = this.rightDataset
      this.updateMappingsCombobox(dataset, position)
      this.changeRightMapping(Array<MappingNode>()),
      this.rightInfo = {
        title: this.rightDataset.metadata.title,
        description: this.rightDataset.metadata.description,
        url: this.rightDataset.url,
        keywords: this.rightDataset.metadata.keywords,
        collection: this.rightDataset.collection
      }
    }
  },
  watch: {
    leftDataset () {
      const position = Position.Left
      const dataset = this.leftDataset
      this.updateMappingsCombobox(dataset, position)
      this.changeLeftMapping(Array<MappingNode>())
      this.leftInfo = {
        title: this.leftDataset.metadata.title,
        description: this.leftDataset.metadata.description,
        url: this.leftDataset.url,
        keywords: this.leftDataset.metadata.keywords,
        collection: this.leftDataset.collection
      }
    },
    rightDataset () {
      const position = Position.Right
      const dataset = this.rightDataset
      this.updateMappingsCombobox(dataset, position)
      this.changeRightMapping(Array<MappingNode>())
      this.rightInfo = {
        title: this.rightDataset.metadata.title,
        description: this.rightDataset.metadata.description,
        url: this.rightDataset.url,
        keywords: this.rightDataset.metadata.keywords,
        collection: this.rightDataset.collection
      }
    }
  },
  methods: {
    ...mapActions(STORE_NAME, {
      updateCircleCanvas: Actions.UPDATE_CIRCLE_CANVAS,
      updateTreeCanvas: Actions.UPDATE_TREE_CANVAS
    }),
    ...mapMutations(STORE_NAME, {
      changeLeftMappingList: Mutations.CHANGE_LEFT_MAPPING_LIST,
      changeRightMappingList: Mutations.CHANGE_RIGHT_MAPPING_LIST,
      changeLeftMapping: Mutations.CHANGE_LEFT_MAPPING,
      changeRightMapping: Mutations.CHANGE_RIGHT_MAPPING,
      changeRootId: Mutations.CHANGE_ROOT_ID,
      changeActivePath: Mutations.CHANGE_ACTIVE_PATH,
      changeVisitedNodes: Mutations.CHANGE_VISITED_NODES,
      initPathNodes: Mutations.CHANGE_PATH_NODES
    }),
    initializeVisualisation: function () {
      this.changeRootId(ROOT_ID)
      this.changeActivePath(undefined)
      this.changeVisitedNodes([createVisitedNode(ROOT_ID, ROOT_LABEL)])
      this.initPathNodes()
    },
    updateVisualisation: function () {
      if (this.activeView === 1) {
        this.updateCircleCanvas()
      }
      if (this.activeView === 2) {
        this.updateTreeCanvas()
      }
    },
    mappingChoosed: function (position: Position, id: number) {
      switch (position) {
        case Position.Left:
          this.leftMappingTree = createMapping(this.labels, this.leftDataset, id)
          break
        case Position.Right:
          this.rightMappingTree = createMapping(this.labels, this.rightDataset, id)
          break
      }
    },
    mappingChanged: function (position: Position, array: Array<MappingNode>) {
      switch (position) {
        case Position.Left:
          this.changeLeftMapping(array)
          break
        case Position.Right:
          this.changeRightMapping(array)
          break
      }
      this.updateVisualisation()
    },
    updateMappingsCombobox: function (dataset: any, position: Position) {
      const result: Array<ComboboxItem> = []
      dataset.mappings.forEach((element: {data: [], metadata: {from: string, title: string, input: []}}, i: number) => {
        addMappingItemToArray(result, element, i)
      })
      result.push(new ComboboxItem('All', result.length))
      switch (position) {
        case Position.Left:
          this.changeLeftMappingList(result)
          break
        case Position.Right:
          this.changeRightMappingList(result)
          break
      }
    }
  }
})
</script>

<style>
.circle {
  cursor: pointer;
  text-decoration: underline;
}
.labels {
  cursor: pointer;
  text-anchor: middle;
  pointer-events: none;
}
</style>
