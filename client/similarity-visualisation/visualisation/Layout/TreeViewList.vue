<template>
  <v-treeview
    style="overflow-y: auto; height: 70vh"
    v-model="selectedItems"
    :items="items"
    selectable
    @input="selectedChanged"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import { MappingNode } from '../../models/MappingNode'
import { mapGetters, mapMutations } from 'vuex'
import { STORE_NAME, Getters, Mutations } from '../Visualisation.store'
import { Position } from '../../models'

export default Vue.extend({
  name: 'TreeViewList',

  props: ['items', 'position'],
  data: () => ({
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      hierarchy: Getters.GET_HIERARCHY,
      leftItems: Getters.GET_LEFT_SELECTED_ITEMS,
      rightItems: Getters.GET_RIGHT_SELECTED_ITEMS
    }),
    selectedItems: {
      get: function () {
        if (this.$props.position === Position.Left) {
          return this.leftItems
        } else {
          return this.rightItems
        }
      },
      set: function (value) {
        if (this.$props.position === Position.Left) {
          this.$store.commit(STORE_NAME + '/' + Mutations.CHANGE_LEFT_SELECTED_ITEMS, value)
        } else {
          this.$store.commit(STORE_NAME + '/' + Mutations.CHANGE_RIGHT_SELECTED_ITEMS, value)
        }
      }
    }
  },
  methods: {
    selectedChanged: function (data: [number]): void {
      const array = Array<MappingNode>()
      const tmpArray: Array<MappingNode> = this.items
      tmpArray.forEach(element => {
        if (element.children !== undefined) {
          element.children.forEach(element => {
            array.push(element)
          })
        }
      })
      const result = Array<MappingNode>()
      data.forEach((element: number) => {
        const node = array.filter(x => x.id === element)[0]
        if (node !== undefined) {
          result.push(node)
        }
      })
      this.$emit('selectedItems', result)
    }
  }
})
</script>
