<template>
  <v-container class="text-center" fluid>
    <h1>Tutorial</h1>
    <div>
      <section>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/sgWFqfthw-8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </section>
    </div>
    <div v-for="(image, index) in images" v-bind:key="index">
      <h2>
        {{ titles[index] }}
      </h2>
      <img
        class="tutorial-image"
        :src="`./images/${image}.png`"
        :alt="titles[index]"
      />
      <p>{{ texts[index] }}</p>
    </div>
  </v-container>
</template>

<script>

export default {
  "name": "evaluation",
  "data": () => ({
    "images": [
      "add_dataset",
      "choose_map_by",
      "choosing_mapping",
      "zooming",
      "adding_paths",
      "paths",
      "paths-tree",
      "tree",
    ],
    "titles": [
      "Add dataset",
      "Choose map by",
      "Choosing mapping",
      "Zooming",
      "Adding paths",
      "Paths",
      "Paths tree",
      "Tree",
    ],
    "texts": [
      "Add url of file with hierarchy and mapping.",
      "Select based on what you want to map to hierarchy.",
      "Tick the words you want to see where it is mapped.",
      // eslint-disable-next-line
      "With the slider you can specify the descendants of what level you will see.",
      // eslint-disable-next-line
      "Add a link to a file where the similarity paths between the two selected datasets are.",
      // eslint-disable-next-line
      "Select a pair to display an explanation of their similarity in the graph.",
      "You can switch to the tree view",
      // eslint-disable-next-line
      "In the tree structure, click the entity, if it is a leaf, to expand its subtree. If not, hide its subtree.",
    ],
  }),
};

</script>

<style>
.tutorial-image{
  width: 100%;
  max-width: 720px;
}
</style>
