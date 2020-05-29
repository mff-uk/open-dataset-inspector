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
          mdi-settings
        </v-icon>
      </v-btn>
    </template>
    <v-btn
      v-tippy="{ 'placement' : 'left' }"
      fab
      dark
      color="blue"
      content="Open mapping dialog"
      @click="$emit('show-mapping-dialog')"
    >
      <v-icon dark>
        mdi-decagram
      </v-icon>
    </v-btn>
    <v-btn
      v-tippy="{ 'placement' : 'left' }"
      fab
      dark
      color="blue"
      content="Open path dialog"
      @click="$emit('show-path-dialog')"
    >
      <v-icon dark>
        mdi-decagram
      </v-icon>
    </v-btn>
    <v-btn
      v-tippy="{ 'placement' : 'left' }"
      fab
      dark
      color="blue"
      content="Open highlight dialog"
      @click="$emit('show-highlight-dialog')"
    >
      <v-icon dark>
        mdi-decagram
      </v-icon>
    </v-btn>
  </v-speed-dial>
</template>

<script>
export default {
  "name": "dialog-menu",
  "data": () => ({
    "showSpeedDial": false,
  }),
};
</script>
