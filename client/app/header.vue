<template>
  <v-app-bar
    color="green"
    dark
    app
  >
    <v-toolbar-title class="title">
      Open Dataset Inspector
    </v-toolbar-title>
    <v-btn
      :to="{'name':'evaluation'}"
      text
    >
      Evaluation
    </v-btn>
    <v-btn
      :to="{'name':'exploration'}"
      text
    >
      Exploration
    </v-btn>
    <v-btn
      :to="{'name':'visualisation'}"
      text
    >
      Visualisation
    </v-btn>
    <v-btn
      :to="{'name':'tutorial'}"
      text
    >
      Tutorial
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  "name": "app-header",
  "data": () => ({}),
};
</script>

<style scoped>
  .title {
    margin-right: 1rem;
  }
</style>
