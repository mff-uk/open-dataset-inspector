import { register } from "../app/register.ts";
import tutorialComponent from "./tutorial.vue";

register({
  "path": "/tutorial",
  "name": "tutorial",
  "component": tutorialComponent,
});
