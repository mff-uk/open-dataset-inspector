<template>
  <svg id="svg" ref="svg" width="100%" height="70vh">
    <g>
      <template v-for="(c, index) in links">
        <tree-link class="movable" v-bind:key="index" v-bind:linkData="c"></tree-link>
      </template>
    </g>
    <g>
      <template v-for="(c, index) in circles">
        <tree-node class="movable" @nodeClicked="nodeClicked" v-bind:key="index" v-bind:nodeData="c"></tree-node>
      </template>
    </g>
    <g>
      <template v-for="(c, index) in circles">
        <tree-label class="movable" @labelClicked='nodeClicked' v-bind:key="index" v-bind:labelData="c"></tree-label>
      </template>
    </g>
  </svg>
</template>

<script lang="ts">
import Vue from 'vue'
import * as d3 from 'd3'
import TreeNode from './TreeNode.vue'
import TreeLink from './TreeLink.vue'
import TreeLabel from './TreeLabel.vue'
import { mapGetters, mapActions, mapMutations } from 'vuex'
import { Actions, Getters, Mutations, STORE_NAME } from '../Visualisation.store'
import { Circle, Position, ROOT_ID, ROOT_LABEL } from '../../models'
import { createNodes, createLabel } from '../../utils/nodesUtils'
import { createLabels, createHierarchy } from '../../utils/hierarchyUtils'

export default Vue.extend({
  name: 'TreeVisualisation',
  components: {
    TreeNode,
    TreeLink,
    TreeLabel
  },
  props: ['rightDataset', 'leftDataset', 'activeView'],
  data: () => ({
    left: Position.Left,
    right: Position.Right
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      circles: Getters.GET_TREE_NODES,
      links: Getters.GET_TREE_LINKS,
      labels: Getters.GET_LABELS,
      hierarchy: Getters.GET_HIERARCHY
    })
  },
  created () {
    window.addEventListener('resize', this.handleResize)
  },
  destroyed () {
    window.removeEventListener('resize', this.handleResize)
  },
  mounted () {
    if (this.rightDataset !== undefined || this.leftDataset !== undefined) {
      this.initLabelsAndNodes()
    }
    this.resizeCanvas({
      // @ts-ignore
      height: this.$refs.svg.clientHeight,
      // @ts-ignore
      width: this.$refs.svg.clientWidth
    })

    this.updateVisualisation()

    const g = d3.selectAll('g')

    /* eslint-disable no-undef */
    // @ts-ignore
    d3.select('#svg')
      // @ts-ignore
      .call(d3.zoom().on('zoom', function () {
        g.attr('transform', d3.event.transform)
      }))
    /* eslint-enable no-undef */
    // 'translate(' + d3.event.translate + ')scale(' + d3.event.scale + ')'
  },
  watch: {
    rightDataset () {
      this.updateVisualisation()
    },
    leftDataset () {
      this.updateVisualisation()
    }
  },
  methods: {
    ...mapActions(STORE_NAME, {
      resizeCanvas: Actions.RESIZE_CANVAS,
      appendNode: Actions.APPEND_NODE_TREE,
      cutChildren: Actions.CUT_NODE_TREE_CHILDREN,
      createHierarchyForTree: Actions.CREATE_HIERARCHY_FOR_TREE,
      updateTreeCanvas: Actions.UPDATE_TREE_CANVAS
    }),
    ...mapMutations(STORE_NAME, {
      changeLeftMapping: Mutations.CHANGE_LEFT_MAPPING,
      changeRightMapping: Mutations.CHANGE_RIGHT_MAPPING,
      changeNodes: Mutations.CHANGE_NODES,
      changeHierarchy: Mutations.CHANGE_HIERARCHY,
      changeLabels: Mutations.CHANGE_LABELS
    }),
    updateVisualisation: function () {
      this.createHierarchyForTree()
      this.updateTreeCanvas()
    },
    handleResize () {
      this.resizeCanvas({
        // @ts-ignore
        height: this.$refs.svg.clientHeight,
        // @ts-ignore
        width: this.$refs.svg.clientWidth
      })
      this.updateTreeCanvas()
    },
    nodeClicked (item: Circle) {
      if (item.isLeaf) {
        this.appendNode(item)
      } else {
        this.cutChildren(item)
      }
    },
    initLabelsAndNodes: function () {
      this.changeLabels(createLabels(this.leftDataset, this.rightDataset))
      this.changeHierarchy(createHierarchy(this.leftDataset, this.rightDataset))
      this.changeNodes(createNodes(this.hierarchy, this.labels))
    }
  }
})
</script>

<style>
.circle {
  cursor: pointer;
  text-decoration: underline;
}
.tree-labels {
  cursor: pointer;
  text-anchor: middle;
  pointer-events: none;
}
</style>
