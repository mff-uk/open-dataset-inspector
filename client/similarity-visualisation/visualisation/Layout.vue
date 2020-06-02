<template>
    <v-container>
      <v-row>
        <v-col cols="2">
        </v-col>
        <v-col cols="8">
          <v-col cols="12">
            <v-row>
              <History-bar
                v-if="historyBarVisible"
                v-bind:activeView="activeView"
              ></History-bar>
            </v-row>
            <v-row class="text-center">
              <value-slider
                v-if="activeView === 1"
              ></value-slider>
            </v-row>
            <v-row class="text-center">
              <path-bar
                v-bind:paths="paths"
                @cancelClicked='cancelClicked'
                @pathUpdated='pathUpdated'
              >
              </path-bar>
            </v-row>
          </v-col>
        </v-col>
        <v-col cols="2">
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import Vue from 'vue'
import ValueSlider from './Layout/ValueSlider.vue'
import HistoryBar from './Layout/HistoryBar.vue'
import PathBar from './Layout/PathBar.vue'
import { Actions, Mutations, Getters, STORE_NAME } from './Visualisation.store'
import { mapActions, mapMutations, mapGetters } from 'vuex'
import { ROOT_LABEL, ROOT_ID, MAX_TREE_DEPTH } from '../models'
import { createVisitedNode } from '../utils/nodesUtils'
import { createPaths } from '../utils/pathUtils'

export default Vue.extend({
  name: 'Layout',
  components: {
    ValueSlider,
    HistoryBar,
    PathBar
  },
  props: ['rightDataset', 'leftDataset', 'pathsDataset', 'activeView', 'labels'],
  data: () => ({
    paths: undefined,
    historyBarVisible: true
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      nodes: Getters.GET_NODES,
      activePath: Getters.GET_ACTIVE_PATH
    })
  },
  watch: {
    pathsDataset () {
      this.updatePaths()
    },
    leftDataset () {
      this.updatePaths()
    },
    rightDataset () {
      this.updatePaths()
    }
  },
  mounted () {
    if (this.leftDataset !== undefined) {
      this.updatePaths()
    }
    if (this.rightDataset !== undefined) {
      this.updatePaths()
    }
    if (this.pathsDataset !== undefined) {
      this.updatePaths()
    }
  },
  methods: {
    ...mapActions(STORE_NAME, {
      createHierarchyForCircles: Actions.CREATE_HIERARCHY_FOR_CIRCLES,
      createHierarchyForTree: Actions.CREATE_HIERARCHY_FOR_TREE,
      updateCircleCanvas: Actions.UPDATE_CIRCLE_CANVAS,
      updateTreeCanvas: Actions.UPDATE_TREE_CANVAS,
      selectPath: Actions.SELECT_PATH
    }),
    ...mapMutations(STORE_NAME, {
      changeActivePath: Mutations.CHANGE_ACTIVE_PATH,
      changeRootId: Mutations.CHANGE_ROOT_ID,
      changePathNodes: Mutations.CHANGE_PATH_NODES,
      changeVisitedNodes: Mutations.CHANGE_VISITED_NODES,
      changeLeftMapping: Mutations.CHANGE_LEFT_MAPPING,
      changeRightMapping: Mutations.CHANGE_RIGHT_MAPPING
    }),
    updatePaths: function () {
      this.historyBarVisible = true
      if (this.pathsDataset !== undefined) {
        this.pathsVisible = true
        this.paths = createPaths(this.nodes, this.pathsDataset, this.labels)
      }
      this.changeActivePath(undefined)
    },
    cancelClicked: function () {
      this.historyBarVisible = true
      this.changeLeftMapping([])
      this.changeRightMapping([])
      this.changeRootId(ROOT_ID)
      this.changeVisitedNodes([createVisitedNode(ROOT_ID, ROOT_LABEL)])
      this.changePathNodes([])
      this.changeActivePath(undefined)
      switch (this.activeView) {
        case 1:
          this.createHierarchyForCircles()
          this.updateCircleCanvas()
          break
        case 2:
          this.createHierarchyForTree(MAX_TREE_DEPTH)
          this.updateTreeCanvas()
          break
      }
    },
    pathUpdated: function () {
      this.historyBarVisible = false
      this.selectPath(this.labels)
      switch (this.activeView) {
        case 1:
          this.createHierarchyForCircles()
          this.updateCircleCanvas()
          break
        case 2:
          this.createHierarchyForTree(this.activePath.height)
          this.updateTreeCanvas()
          break
      }
    }
  }
})
</script>

<style>
.btn-nodes {
  font-size: 8;
}
</style>
