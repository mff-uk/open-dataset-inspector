<template>
  <text class="circle-labels"
    fill="white"
    :x="labelData.x"
    v-if="labelData.isLeaf && labelData.r > 5"
    :font-size="labelData.r > 60 ? 30 : labelData.r / 2"
    :y="labelData.y"
    dy=".35em"
    @click.exact="emit(labelData)"
    @click.ctrl="openWiki(labelData)"
  >
    <tspan v-if="labelData.label.length >= 18 && labelData.r < 120" :x="labelData.x" dy="-0.6em">{{ labelData.label.substring(0, 5) + "-" }}</tspan>
    <tspan v-if="labelData.label.length >= 18 && labelData.r < 120" :x="labelData.x" dy="1em">{{ labelData.label.substring(5, 13) + "-" }}</tspan>
    <tspan v-if="labelData.label.length >= 18 && labelData.r < 120" :x="labelData.x" dy="1em">{{ labelData.label.length > 18 ? labelData.label.substring(13, 18) + ".." : labelData.label.substring(13, 18) }}</tspan>

    <tspan v-if="labelData.label.length >= 18 && labelData.r >= 120" :x="labelData.x" dy="0.3em">{{ labelData.label }}</tspan>

    <tspan v-if="labelData.label.length < 18 && labelData.label.length > 6 && labelData.r < 80" :x="labelData.x" dy="0em">{{ labelData.label.substring(0, 6) + "-" }}</tspan>
    <tspan v-if="labelData.label.length < 18 && labelData.label.length > 6 && labelData.r < 80" :x="labelData.x" dy="1em">{{ labelData.label.length > 12 ? labelData.label.substring(6, 12) + ".." : labelData.label.substring(6, 12) }}</tspan>

    <tspan v-if="labelData.label.length < 18 && labelData.label.length > 6 && labelData.r >= 80" :x="labelData.x" dy="0.3em">{{ labelData.label }}</tspan>

    <tspan v-if="labelData.label.length <= 6" :x="labelData.x" dy="0.3em">{{ labelData.label.substring(0, 7) }}</tspan>
  </text>
</template>

<script lang="ts">
import Vue from 'vue'
import { Circle } from '../../models'

export default Vue.extend({
  name: 'CircleLabel',
  props: {
    labelData: {
      type: Object
    }
  },
  data: () => ({
  }),
  computed: {
  },
  methods: {
    /** @param {MouseEvent} event */
    emit (event: Circle) {
      this.$emit('labelClicked', event)
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

<style>
.circle-labels {
  cursor: pointer;
  text-anchor: middle;
  pointer-events: none;
}
</style>
