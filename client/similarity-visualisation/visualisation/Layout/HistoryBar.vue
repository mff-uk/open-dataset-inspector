<template>
  <v-content>
    <p>Visited nodes</p>
    <template v-for="(c, index) in visitedNodes">
      <v-btn
        v-bind:content="`
          label: ${c.label}</br>
          id: ${c.id}
        `"
        v-tippy='{interactive : true, animateFill: false, placement:"left", animation:"shift-toward", delay:10, arrow : true}'
        v-bind:key="index"
        class="btn-help ma-2" @click="click(index)"
        outlined
        large
        fab
        color="black"
      >
        {{ c.label.length > 5 ? c.label.substring(0, 5) + ".." : c.label }}
      </v-btn>
    </template>
  </v-content>
</template>

<script lang="ts">
import Vue from 'vue'
import { Getters, Actions, STORE_NAME } from '../Visualisation.store'
import { mapGetters, mapActions } from 'vuex'
import { Label } from '../../models'

export default Vue.extend({
  name: 'HistoryBar',

  data: () => ({
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      visitedNodes: Getters.GET_VISITED_NODES
    })
  },
  methods: {
    ...mapActions(STORE_NAME, {
      updatePath: Actions.UPDATE_PATH
    }),
    click: function (data: Label) {
      this.updatePath(data)
    }
  }
})
</script>

<style>
.btn-help {
  text-transform: none;
}
.circle {
  cursor: pointer;
}
.labels {
  cursor: pointer;
  text-anchor: middle;
  pointer-events: none;
}
</style>
