import VueRouter from "vue-router";
import { getRegistered } from "./register.ts";

const router = new VueRouter({
  "routes": getRegistered()
    .filter((item) => item.path !== undefined)
    .map((item) => ({
      "path": item.path,
      "name": item.name,
      "component": item.component,
    })),
});

export default router;
