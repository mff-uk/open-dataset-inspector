<template>
  <v-container fluid>
    <query-panel
      :task="task"
      :query="query"
      :description="description"
      @search="onSearch"
      @user="setUser"
      @use-case-id="setUseCaseId"
      @use-case="setUseCase"
    />
    <br>
    <method-array
      :datasets="datasets"
      :methods="methods"
      :highlights="highlights"
      :ratings="ratings"
      @change-order="onChangeOrder"
      @change-method-rating="onChangeMethodRating"
    />
    <div class="d-flex flex-row-reverse footer">
      <v-btn
        color="primary"
        :disabled="!allowSubmit"
        @click="onSubmitAndClear"
      >
        Submit & clear
      </v-btn>
    </div>
    <v-dialog
      v-model="dialog.visible"
      max-width="600px"
    >
      <v-card>
        <v-card-title class="headline">
          {{ dialog.title }}
        </v-card-title>
        <v-card-text>
          {{ dialog.body }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="green darken-1"
            text
            @click="dialog.visible = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import randomColor from "randomcolor";
import MethodArray from "./method-array.vue";
import QueryPanel from "./query-panel.vue";
import {
  fetchSimilarDatasets,
  shuffleArray,
  postEvaluation,
} from "./evaluation-service.ts";
import {
  queryParamsToDatasetString,
  datasetStringToArray,
} from "../utils.ts";
import { required, decimal } from "./validators.ts";

export default {
  "name": "evaluation",
  "components": {
    "method-array": MethodArray,
    "query-panel": QueryPanel,
  },
  "data": () => ({
    "task": {
      "timeSession": new Date().toISOString(),
      "session": uuidv4(),
      "user": loadUser(),
      "useCaseId": "",
      "useCase": "",
      "index": 0,
    },
    "query": {
      "dataset": "",
      "group": "",
    },
    "datasets": {},
    "methods": [],
    "description": "",
    "highlights": {},
    "queryDatasets": [],
    "ratings": {},
    "dialog": {
      "visible": false,
      "title": "",
      "body": "",
    },
  }),
  "computed": {
    "allowSubmit": function () {
      const methodsLength = this.methods.length;
      const ratings = Object.values(this.ratings);
      if (methodsLength === 0) {
        return false;
      }
      for (const value of ratings) {
        if (!required(value) || !decimal(value)) {
          return false;
        }
      }
      return true;
    },
  },
  "mounted": function () {
    this.query = {
      "dataset": queryParamsToDatasetString(this.$route.query.dataset),
      "group": this.$route.query.group || "round-000",
    };
    this.load();
  },
  "methods": {
    "load": function () {
      const options = {
        "count": this.$route.query.count || 7,
      };
      this.queryDatasets = datasetStringToArray(this.query.dataset);
      fetchSimilarDatasets(this.query.group, this.queryDatasets, options)
        .then((result) => {
          if (this.queryDatasets.length > 0 && result.methods.length === 0) {
            throw new Error("No similarities found, please check your query.");
          }
          shuffleArray(result.methods);
          this.methods = result.methods;
          this.datasets = result.datasets;
          this.description = result.description;
          this.ratings = {};
          this.methods.forEach((method, index) => {
            this.ratings[method.id] = String(index);
          });
          this.task.timeLoad = new Date().toISOString();
        }).then(() => {
          this.highlights = createHighlight(this.methods);
        }).catch((error) => {
          this.dialog = {
            "visible": true,
            "title": "Can't load datasets",
            "body": error,
          };
        });
    },
    "onChangeOrder": function (methods) {
      // We preserve ratings for methods, that did not moved.
      const nextRatings = {};
      methods.forEach((method, index) => {
        if (method.id === this.methods[index].id) {
          // No change in position.
          nextRatings[method.id] = this.ratings[method.id];
        } else {
          nextRatings[method.id] = String(index);
        }
      });
      //
      this.ratings = nextRatings;
      this.methods = methods;
      //
      this.onSubmit("change-method-order");
    },
    "onChangeMethodRating": function (event) {
      this.ratings = {
        ...this.ratings,
        [event.method.id]: String(event.value),
      };
      //
      this.onSubmit("change-method-order-number");
    },
    "onSearch": function (search) {
      this.query = {
        ...this.query,
        ...search,
      };
      const dataset = datasetStringToArray(search.dataset);
      this.$router.push({
        "path": "evaluation",
        "query": {
          ...this.$route.query,
          ...this.query,
          "dataset": dataset,
        },
      });
      this.load(false);
    },
    "onSubmit": function (action) {
      saveUser(this.task.user);
      this.task.index += 1;
      return postEvaluation({
        "task": {
          ...this.task,
          "action": action,
          "group": this.query.group,
          "valid": this.allowSubmit,
          "query": this.queryDatasets,
          "timePost": new Date().toISOString(),
        },
        "rating": this.ratings,
        "data": this.methods.map((method) => ({
          "id": method.id,
          "numSameScoreAsLast": method.numSameScoreAsLast,
          "datasets": method.datasets,
        })),
      });
    },
    "onSubmitAndClear": function () {
      this.onSubmit("submit").then(() => {
        this.query = {
          ...this.query,
          "dataset": "",
        };
        this.task = {
          ...this.task,
          "useCase": "",
          "index": 0,
        };
        this.methods = [];
        this.highlights = {};
        this.queryDatasets = [];
        this.ratings = {};
        this.$router.push({
          "path": "evaluation",
          "query": {
            ...this.$route.query,
            "dataset": undefined,
          },
        });
      }).catch((error) => {
        this.dialog = {
          "visible": true,
          "title": "Can't save data",
          "body": error,
        };
      });
    },
    "setUser": function (value) {
      this.task.user = value;
    },
    "setUseCaseId": function (value) {
      this.task.useCaseId = value;
    },
    "setUseCase": function (value) {
      this.task.useCase = value;
    },
  },
};

function uuidv4() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    .replace(/[xy]/g, (c) => {
      // eslint-disable-next-line no-bitwise
      const r = Math.random() * 16 | 0;
      // eslint-disable-next-line no-bitwise,no-mixed-operators
      const v = c === "x" ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
}

function createHighlight(methods) {
  const allDatasets = {};
  for (const method of methods) {
    for (const dataset of method.datasets) {
      allDatasets[dataset.iri] = (allDatasets[dataset.iri] || 0) + 1;
    }
  }
  const sharedDatasets = [];
  for (const [iri, count] of Object.entries(allDatasets)) {
    if (count < 2) {
      continue;
    }
    sharedDatasets.push(iri);
  }
  const colors = generateHlsColors(sharedDatasets.length);
  const result = {};
  sharedDatasets.forEach((iri, index) => {
    result[iri] = colors[index];
  });
  return result;
}

// eslint-disable-next-line no-unused-vars
function generateColorsWithRandomColor(count) {
  return randomColor({
    "format": "hls",
    "count": count,
    "luminosity": "bright",
  });
}

function generateHlsColors(count) {
  const result = [];
  for (let x = 0; x < count; x += 1) {
    // eslint-disable-next-line no-mixed-operators
    const hls = (x * (360 / count) % 360);
    result.push(`hsl(${hls},100%,70%)`);
  }
  return result;
}

function loadUser() {
  if (typeof (Storage) === "undefined") {
    return "";
  }
  return localStorage.getItem("user") || "";
}

function saveUser(user) {
  if (user === "") {
    return;
  }
  if (typeof (Storage) === "undefined") {
    return;
  }
  localStorage.setItem("user", user);
}

</script>

<style scoped>
  .footer {
    margin: 0 1rem 1rem 1rem;
  }
</style>
