import Vue from "vue";
import VueRouter from "vue-router";
import Vuetify from "vuetify";
import Vuex from "vuex";
import VueTippy from "vue-tippy";

import "vuetify/dist/vuetify.min.css";

import "./modules";
import App from "./app/app.vue";
import router from "./app/router";
import createStore from "./app/store";

import "./visualisation";

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(Vuetify);
Vue.use(VueTippy);
Vue.use(Vuex);

/* eslint-disable no-new */
new Vue({
  "el": "#app",
  "router": router,
  "store": createStore(),
  "vuetify": new Vuetify({}),
  "render": (h) => h(App),
  "created": () => {
    // this.$store.dispatch('getUsers')
  },
});
