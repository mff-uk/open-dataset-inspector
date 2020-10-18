<template>
    <circle
        v-bind:content="`
          label: ${nodeData.label}</br>
          id: ${nodeData.id}
        `"
        v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
        class="circle"
        :id="nodeData.id"
        :r="nodeData.r"
        :cx="nodeData.x"
        :cy="nodeData.y"
        :fill="nodeData.fill"
        :stroke="nodeData.stroke"
        :stroke-width="nodeData.strokewidth"
        @click.exact="emit(nodeData)"
        @click.ctrl="openWiki(nodeData)"
    >
    </circle>
</template>

<script lang="ts">
import Vue from 'vue'
import { Circle } from '../../models'

export default Vue.extend({
  name: 'TreeNode',
  props: {
    nodeData: {
      type: Object,
      required: true
    }
  },
  data: () => ({
  }),
  computed: {
  },
  methods: {
    /** @param {MouseEvent} event */
    emit (event: Circle) {
      this.$emit('nodeClicked', event)
    },
    // eslint-disable-next-line
    openWiki: function (data: Circle) {
      const win = window.open('https://www.wikidata.org/wiki/' + data.id, '_blank')
      if (win !== null) {
        win.focus()
      }
    }
  }
})
</script>
