<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn
        v-bind:content="`Show tutorial`"
        v-tippy='{interactive : true, animateFill: false, placement:"right", animation:"shift-toward", delay:100, arrow : true}'
        fab
        dark
        small
        v-on="on"
        color="indigo"
      >
        <v-icon>mdi-lifebuoy</v-icon>
      </v-btn>
    </template>
        <v-carousel
          light
          hide-delimiters
          show-arrows-on-hover
          height="80vh"
        >
          <v-carousel-item
            v-for="(image, index) in images"
            :key="index"
          >
            <v-sheet
              height="100%"
              color="white"
            >
              <img
                class="carousel-image"
                :src="`./images/${image}.png`"
                :alt="titles[index]"
              />
              <div class="carousel-title">
                {{ titles[index] }}
              </div>
              <div class="carousel-text">
                {{ texts[index] }}
              </div>
            </v-sheet>
          </v-carousel-item>
      </v-carousel>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'Tutorial',

  data: () => ({
    dialog: false,
    images: [
      'add_dataset',
      'choose_map_by',
      'choosing_mapping',
      'zooming',
      'adding_paths',
      'paths',
      'paths-tree',
      'tree'
    ],
    titles: [
      'Add dataset',
      'Choose map by',
      'Choosing mapping',
      'Zooming',
      'Adding paths',
      'Paths',
      'Paths tree',
      'Tree'
    ],
    texts: [
      'Add url of file with hierarchy and mapping.',
      'Select based on what you want to map to hierarchy.',
      'Tick the words you want to see where it is mapped.',
      'With the slider you can specify the descendants of what level you will see.',
      'Add a link to a file where the similarity paths between the two selected datasets are.',
      'Select a pair to display an explanation of their similarity in the graph.',
      'You can switch to the tree view',
      'In the tree structure, click the entity, if it is a leaf, to expand its subtree. If not, hide its subtree.'
    ]
  }),
  computed: {
  },
  methods: {
  }
})
</script>

<style>
  .carousel-image {
    height: 90%;
  }
</style>
