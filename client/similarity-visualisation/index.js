import { register } from "../app/register.ts";
import { default as store, STORE_NAME } from "./visualisation/Visualisation.store.ts";

export {default as SimilarityVisualisation} from "./similarity-visualisation.vue";

register({
  "name": "similarity-visualisation",
  "store": store,
  "store-name": STORE_NAME,
});
