import { register } from "../app/register.ts";
import explorationComponent from "./similarity-search.vue";

register({
  "path": "/search",
  "name": "search",
  "component": explorationComponent,
});
