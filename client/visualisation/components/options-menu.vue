<template>
  <v-btn
    color="blue darken-2"
    dark
    fab
    @click="$emit('show-options-dialog')"
  >
    <v-icon>
      mdi-settings
    </v-icon>
  </v-btn>
</template>

<script>
export default {
  "name": "options-menu",
  "data": () => ({}),
};
</script>
