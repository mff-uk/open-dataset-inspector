<template>
  <v-speed-dial
    v-model="floatingActionBtnVisible"
    absolute
    right
    bottom
  >
    <template v-slot:activator>
      <v-btn
        v-model="floatingActionBtnVisible"
        color="blue darken-2"
        dark
        fab
      >
        <v-icon v-if="floatingActionBtnVisible">mdi-close</v-icon>
        <v-icon v-else>mdi-menu</v-icon>
      </v-btn>
    </template>
    <add-path-dialog @pathsDatasetChanged="pathsDatasetChanged"></add-path-dialog>
    <v-dialog v-model="leftDialogDisplay" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn
          fab
          small
          color="primary"
          v-on="on"
          v-bind:content="`Change left dataset`"
          v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
        >
          <v-icon>mdi-set-left</v-icon>
      </v-btn>
      </template>
      <add-dataset-form
        @datasetChanged="leftDatasetChanged"
        @dialogClosed="dialogClosed"
      >
      </add-dataset-form>
    </v-dialog>
    <v-dialog v-model="rightDialogDisplay" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <v-btn
          fab
          small
          color="primary"
          v-on="on"
          v-bind:content="`Change right dataset`"
          v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
        >
          <v-icon>mdi-set-right</v-icon>
      </v-btn>
      </template>
      <add-dataset-form @datasetChanged="rightDatasetChanged" @dialogClosed="dialogClosed"></add-dataset-form>
    </v-dialog>
    <v-btn
      v-bind:content="`Switch to tree view`"
      v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
      fab
      dark
      small
      @click="viewTree"
    >
      <v-icon>mdi-graph</v-icon>
    </v-btn>
    <v-btn
      v-bind:content="`Switch to circle view`"
      v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
      fab
      dark
      small
      @click="viewCircles"
    >
      <v-icon>mdi-chart-bubble</v-icon>
    </v-btn>
    <tutorial></tutorial>
  </v-speed-dial>
</template>

<script lang='ts'>
import Vue from 'vue'
import axios from 'axios'
import AddPathDialog from '../common-components/AddPathDialog.vue'
import AddDatasetForm from '../common-components/AddDatasetForm.vue'
import Tutorial from '../tutorial/TutorialDialog.vue'

export default Vue.extend({
  name: 'Menu',
  components: {
    AddPathDialog,
    AddDatasetForm,
    Tutorial
  },
  data: () => ({
    leftDialogDisplay: false,
    rightDialogDisplay: false,
    floatingActionBtnVisible: false
  }),
  methods: {
    leftDatasetChanged: function (url: string) {
      this.$emit('leftDatasetChanged', url)
    },
    rightDatasetChanged: function (url: string) {
      this.$emit('rightDatasetChanged', url)
    },
    pathsDatasetChanged: function (url: string) {
      this.$emit('pathsDatasetChanged', url)
    },
    viewCircles: function () {
      this.$emit('setCircleView')
    },
    viewTree: function () {
      this.$emit('setTreeView')
    },
    dialogClosed: function () {
      this.rightDialogDisplay = false
      this.leftDialogDisplay = false
    }
  }
})
</script>
