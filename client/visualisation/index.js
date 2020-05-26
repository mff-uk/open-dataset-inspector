import { register } from "../app/register.ts";
import visualisationComponent from "./visualisation.vue";
import { createStore, STORE_NAME } from "./visualisation-store";

register({
  "path": "/visualisation",
  "name": "visualisation",
  "component": visualisationComponent,
  "store": createStore(),
  "store-name": STORE_NAME,
});
