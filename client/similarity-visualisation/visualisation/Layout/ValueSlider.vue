<template>
  <v-container>
    <p>Level of descendants in the view</p>
    <v-slider
      v-if="minimum !== maximum"
      v-bind:min="minimum"
      v-bind:value="depth"
      v-bind:max="maximum"
      @change="handleDepthChange"
      :thumb-size="24"
      thumb-label="always"
      :color=color
    >
    </v-slider>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapMutations, mapGetters, mapActions } from 'vuex'
import { Mutations, Actions, Getters, STORE_NAME } from '../Visualisation.store'

export default Vue.extend({
  name: 'ValueSlider',

  data: () => ({
    minimum: 1,
    color: '#009DFF'
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      maximum: Getters.GET_MAX_DEPTH,
      depth: Getters.GET_DEPTH
    })
  },
  methods: {
    ...mapMutations(STORE_NAME, {
      changeDepth: Mutations.CHANGE_DEPTH
    }),
    ...mapActions(STORE_NAME, {
      createHierarchyForCircles: Actions.CREATE_HIERARCHY_FOR_CIRCLES,
      updateCircleCanvas: Actions.UPDATE_CIRCLE_CANVAS
    }),
    // eslint-disable-next-line
    handleDepthChange: function (data: any) {
      this.changeDepth(data)
      this.createHierarchyForCircles()
      this.updateCircleCanvas()
    }
  }
})
</script>
