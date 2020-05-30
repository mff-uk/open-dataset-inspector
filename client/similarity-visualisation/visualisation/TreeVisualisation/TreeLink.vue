<template>
    <path class="link"
        :id="linkData.id"
        :d="pathText"
        stroke='black'
        fill='none'
        >
    </path>
</template>

<script lang="ts">
import Vue from 'vue'
import * as d3 from 'd3'

export default Vue.extend({
  name: 'TreeLink',
  props: {
    linkData: {
      type: Object,
      required: true
    }
  },
  data: () => ({
  }),
  computed: {
    pathText: function () {
      // @ts-ignore
      const leftx: number = this.linkData.lx
      const lefty: number = this.linkData.ly
      const rightx: number = this.linkData.rx
      const righty: number = this.linkData.ry
      const left: any = [leftx, lefty]
      const right: any = [rightx, righty]
      return d3.linkVertical()({
        // @ts-ignore
        source: left,
        target: right
      })
    }
  },
  methods: {
  }
})
</script>
