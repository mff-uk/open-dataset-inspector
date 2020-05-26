import Vuex from "vuex";
import { getRegistered } from "./register.ts";

export default function createStore() {
  const modules = {};
  getRegistered()
    .filter((item) => item.store !== undefined)
    .forEach((item) => {
      console.log("store", item);
      modules[item["store-name"]] = item.store;
    });
  return new Vuex.Store({
    "modules": modules,
  });
}
