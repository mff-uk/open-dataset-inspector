<template>
  <v-treeview
    v-model="selectedItems"
    :items="items"
    selectable
    @input="selectedChanged"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import { MappingNode } from '../../models/MappingNode'

export default Vue.extend({
  name: 'TreeViewList',

  props: ['items'],
  data: () => ({
    selectedItems: Array<MappingNode>()
  }),
  computed: {
  },
  methods: {
    // eslint-disable-next-line
    selectedChanged: function (data: any): void {
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
      data.forEach((element: any) => {
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
