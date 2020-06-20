<template>
  <v-speed-dial
    v-model="showSpeedDial"
    transition="scale-transition"
    open-on-hover
  >
    <template v-slot:activator>
      <v-btn
        v-model="showSpeedDial"
        color="blue darken-2"
        dark
        fab
      >
        <v-icon v-if="showSpeedDial">
          mdi-close
        </v-icon>
        <v-icon v-else>
          mdi-eye-outline
        </v-icon>
      </v-btn>
    </template>
    <v-btn
      v-tippy="{ 'placement' : 'left' }"
      fab
      dark
      color="blue"
      content="Use network visualisation"
      @click="$emit('input', 0)"
    >
      <v-icon dark>
        mdi-lan
      </v-icon>
    </v-btn>
    <v-btn
      v-tippy="{ 'placement' : 'left' }"
      fab
      dark
      color="blue"
      content="Use tree visualisation"
      @click="$emit('input', 2)"
    >
      <v-icon dark>
        mdi-file-tree
      </v-icon>
    </v-btn>
    <v-btn
      v-tippy="{ 'placement' : 'left' }"
      fab
      dark
      color="blue"
      content="Use circle visualisation"
      @click="$emit('input', 1)"
    >
      <v-icon dark>
        mdi-google-circles-communities
      </v-icon>
    </v-btn>
  </v-speed-dial>
</template>

<script>
export default {
  "name": "visualisation-menu",
  "data": () => ({
    "showSpeedDial": false,
  }),
};
</script>
