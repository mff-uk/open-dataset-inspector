import { register } from "../app/register.ts";
import component from "./home.vue";

register({
  "path": "/",
  "name": "home",
  "component": component,
});
