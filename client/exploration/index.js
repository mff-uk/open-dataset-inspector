import { register } from "../app/register.ts";
import explorationComponent from "./exploration.vue";

register({
  "path": "/exploration",
  "name": "exploration",
  "component": explorationComponent,
});
