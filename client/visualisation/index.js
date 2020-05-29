import { register } from "../app/register.ts";
import visualisationComponent from "./visualisation.vue";
import { createStore, STORE } from "./visualisation-store";

register({
  "path": "/visualisation",
  "name": "visualisation",
  "component": visualisationComponent,
  "store": createStore(),
  "store-name": STORE,
});
