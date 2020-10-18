<template>
  <v-expansion-panels
    v-model="panels"
    multiple
  >
    <v-expansion-panel>
      <v-expansion-panel-header>
        Instructions
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        {{ description }}
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Query
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-layout
          row
          wrap
        >
          <v-flex
            xs12
            md6
          >
            <v-text-field
              v-model="user"
              label="Tester ID (Optional)"
              @input="setUser"
            />
          </v-flex>
          <v-flex
            xs12
            md6
          >
            <v-text-field
              v-model="useCaseId"
              label="Use-Case ID (Optional)"
              @input="setUseCaseId"
            />
          </v-flex>
        </v-layout>
        <v-textarea
          v-model="useCase"
          label="Use-case"
          @input="setUseCase"
        />
        <v-textarea
          v-model="dataset"
          label="Dataset"
          hint="Dataset IRI"
        />
        <v-btn
          style="float:right;"
          @click="search"
        >
          Search
        </v-btn>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  "name": "query-panel",
  "props": {
    "task": { "type": Object, "required": true },
    "query": { "type": Object, "required": true },
    "description": { "type": String },
  },
  "data": () => ({
    "group": "",
    "dataset": "",
    "user": "",
    "useCaseId": "",
    "useCase": "",
    "panels": [0, 1], // Make the panel open at the start.
  }),
  "mounted": function () {
    this.group = this.query.group;
    this.dataset = this.query.dataset;
    this.user = this.task.user;
    this.useCase = this.task.useCase;
  },
  "watch": {
    "query": function (query) {
      this.group = query.group;
      this.dataset = query.dataset;
    },
    "task": function (task) {
      this.user = task.user;
      this.useCaseId = task.useCaseId;
      this.useCase = task.useCase;
    },
  },
  "methods": {
    "search": function () {
      this.$emit("search", {
        "group": this.group,
        "dataset": this.dataset,
      });
    },
    "setUser": function (value) {
      this.$emit("user", value);
    },
    "setUseCaseId": function (value) {
      this.$emit("use-case-id", value);
    },
    "setUseCase": function (value) {
      this.$emit("use-case", value);
    },
  },
};
</script>
