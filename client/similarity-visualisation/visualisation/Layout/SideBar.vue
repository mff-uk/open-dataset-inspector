<template>
  <v-container>
    <v-card
      v-bind:content="`
        ${title}</br></br>
        ${description}</br>
        Keywords: ${keywordsString}
      `"
      v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
      @click="visitDataset"
      class="mx-auto info-card"
      outlined
    >
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title class="headline mb-1">{{ title }}</v-list-item-title>
          <v-list-item-group>{{ collection }}</v-list-item-group>
          <v-list-item-subtitle>{{ description }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-card>
    <v-select
      :items="selectList"
      item-text="name"
      label="Choose map by:"
      return-object
      @change="changeMapping"
      >
    </v-select>
    <tree-view-list
      v-bind:items="mappingList"
      @selectedItems="selectedChanged"
    >
    </tree-view-list>
  </v-container>
</template>

<script lang='ts'>
import Vue from 'vue'
import TreeViewList from '../Layout/TreeViewList.vue'
import { ComboboxItem } from '../../models/ComboboxItem'
import { Position } from '../../models/Position'
import { MappingNode } from '../../models/MappingNode'
import { STORE_NAME, Getters } from '../Visualisation.store'
import { mapGetters, mapMutations } from 'vuex'

export default Vue.extend({
  name: 'SideBar',
  components: {
    TreeViewList
  },
  props: ['sidebarPosition', 'mappingList', 'title', 'collection', 'description', 'url', 'keywords'],
  data: () => ({
    error: Error()
  }),
  computed: {
    ...mapGetters(STORE_NAME, {
      leftList: Getters.GET_LEFT_MAPPING_LIST,
      rightList: Getters.GET_RIGHT_MAPPING_LIST
    }),
    selectList: function () {
      if (this.$props.sidebarPosition === Position.Left) {
        return this.leftList
      } else {
        return this.rightList
      }
    },
    keywordsString: function () {
      let result: string = ''
      this.keywords.forEach((element: string) => {
        result = element + '  ' + result
      })
      console.log(result)
      return result
    }
  },
  methods: {
    changeMapping: function (data: ComboboxItem) {
      this.$emit('mappingChoosed', this.sidebarPosition, data.id)
    },
    selectedChanged: function (array: Array<MappingNode>) {
      this.$emit('mappingChanged', this.sidebarPosition, array)
    },
    visitDataset: function () {
      const win = window.open(this.url)
      if (win !== null) {
        win.focus()
      }
    }
  }
})
</script>
<style scoped>
</style>
