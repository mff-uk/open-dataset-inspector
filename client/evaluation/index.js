import { register } from "../app/register.ts";
import evaluationComponent from "./evaluation.vue";

register({
  "path": "/evaluation",
  "name": "evaluation",
  "component": evaluationComponent,
});
