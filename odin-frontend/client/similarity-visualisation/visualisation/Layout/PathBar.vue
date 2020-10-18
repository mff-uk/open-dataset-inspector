<template>
  <v-container>
    <v-row>
      <v-select
        v-if="labelsVisible"
        clearable
        @click:clear="cancelClicked"
        v-model="select"
        :items="paths"
        label="Select"
        return-object
        @change="pathUpdated"
      >
        <template slot="selection" slot-scope="data">
          {{ data.item.from }} → {{ data.item.to }}
        </template>
        <template slot="item" slot-scope="data">
          {{ data.item.from }} → {{ data.item.to }}
        </template>
      </v-select>
      <v-select
        v-if="!labelsVisible"
        clearable
        @click:clear="cancelClicked"
        v-model="select"
        :items="paths"
        label="Select"
        return-object
        @change="pathUpdated"
      >
        <template slot="selection" slot-scope="data">
          {{ data.item.leftKeywords }} → {{ data.item.rightKeywords }}
        </template>
        <template slot="item" slot-scope="data">
          {{ data.item.leftKeywords }} → {{ data.item.rightKeywords }}
        </template>
      </v-select>
    </v-row>
    <p>Path nodes</p>
    <template v-for="(c, index) in pathNodes">
      <v-btn
        v-bind:content="`
          label: ${c.label}</br>
          id: ${c.id}
        `"
        v-tippy='{interactive : true, animateFill: false, placement:"left", animation:"shift-toward", delay:10, arrow : true}'
        v-bind:key="index"
        class="btn-help ma-2"
        fab
        @click="pathNodeClicked(c)"
        v-bind:color="c.color"
      >
        {{ c.label.length > 5 ? c.label.substring(0, 5) + ".." : c.label }}
      </v-btn>
      <v-icon v-bind:key="'arrow' + index">{{ activePath.arrows[index] }}</v-icon>
    </template>
    <v-switch v-model="labelsVisible" :label="labelsVisible === true ? `Labels displayed` : `Keywords displayed`"></v-switch>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { Getters, STORE_NAME } from '../Visualisation.store'

export default Vue.extend({
  name: 'PathBar',

  data: () => ({
    keywordsVisible: true,
    labelsVisible: true
  }),
  props: {
    paths: {}
  },
  computed: {
    ...mapGetters(STORE_NAME, {
      pathNodes: Getters.GET_PATH_NODES,
      activePath: Getters.GET_ACTIVE_PATH
    }),
    select: {
      get () {
        return this.activePath
      },
      set (value) {
        this.$store.commit(STORE_NAME + '/CHANGE_ACTIVE_PATH', value)
      }
    }
  },
  methods: {
    pathUpdated: function () {
      this.$emit('pathUpdated')
    },
    cancelClicked: function () {
      this.$emit('cancelClicked')
    },
    pathNodeClicked: function (data: Node) {
      this.$emit('pathNodeClicked', data)
    }
  }
})
</script>

<style>
.btn-help {
  text-transform: none;
}
</style>
