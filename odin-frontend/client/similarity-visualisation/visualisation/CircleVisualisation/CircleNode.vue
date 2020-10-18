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
        @click.exact="emit(nodeData)"
        @click.ctrl="openWiki(nodeData)"
    >
    </circle>
</template>

<script lang="ts">
import Vue from 'vue'
import { Circle } from '../../models'

export default Vue.extend({
  name: 'CircleNode',
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
    emit (circle: Circle) {
      this.$emit('nodeClicked', circle)
    },
    openWiki: function (circle: Circle) {
      const win = window.open('https://www.wikidata.org/wiki/' + circle.id, '_blank')
      if (win !== null) {
        win.focus()
      }
    }
  }
})
</script>
