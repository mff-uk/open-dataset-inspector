<template>
    <line class="link"
        v-bind:content="`
          map by: ${linkData.word}</br>
          map to: ${linkData.mapTo}</br>
          `"
        v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:20, arrow : true}'
        :id="linkData.id"
        :x1="linkData.lx"
        :y1="linkData.ly"
        :x2="linkData.rx"
        :y2="linkData.ry"
        stroke='black'
        stroke-width='2'
        marker-end="url(#arrow)"
        >
    </line>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'CircleLink',
  props: {
    linkData: {
      type: Object,
      required: true
    }
  },
  data: () => ({
  }),
  computed: {
  },
  methods: {
  }
})
</script>
