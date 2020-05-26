import {
  fetchDatasetHierarchy,
  fetchLabels,
} from "./visualisation-api.ts";

export const STORE_NAME = "hierarchy";

const ADD_DATASET_ACTION = "add_dataset";
export const ADD_DATASET = `${STORE_NAME}/${ADD_DATASET_ACTION}`;

const REMOVE_DATASET_ACTION = "remove_dataset";
export const REMOVE_DATASET = `${STORE_NAME}/${REMOVE_DATASET_ACTION}`;

export const GET_DATASETS = "get_datasets";

export const GET_LABELS = "get_labels";

export const GET_NODES = "get_nodes";

export const GET_EDGES = "get_edges";

export const GET_HIERARCHY = "get_hierarchy";

export function createStore() {
  return {
    "namespaced": true,
    "state": {
      "datasets": {},
      "labels": {},
      // Hierarchy data.
      "nodes": {},
      "hierarchy": [],
    },
    "mutations": {
      [createDataset.name]: createDataset,
      [updateDataset.name]: updateDataset,
      [updateHierarchy.name]: updateHierarchy,
      [addLabels.name]: addLabels,
    },
    "getters": {
      [GET_DATASETS]: (state) => Object.values(state.datasets),
      [GET_LABELS]: (state) => state.labels,
      [GET_NODES]: (state) => Object.values(state.nodes),
      [GET_EDGES]: (state) => {
        const result = [];
        state.hierarchy.forEach((edge) => {
          result.push({
            "source": edge[0],
            "target": edge[2],
            "label": edge[1],
          });
        });
        return result;
      },
      [GET_HIERARCHY]: (state) => state.hierarchy,
    },
    "actions": {
      [ADD_DATASET_ACTION]: addDatasetAction,
      // [REMOVE_DATASET_ACTION]: removeDatasetAction,
    },
  };
}

function createDataset(state, event) {
  // We create an empty record, so we can use
  // it in the UI before the datasets is loaded.
  state.datasets = {
    ...state.datasets,
    [event.id]: Object.freeze({
      "url": event.dataset,
      "collection": event.collection,
      "metadata": {
        "title": "",
        "description": "",
        "keywords": [],
      },
      "loaded": false,
      "mappings": [],
      "hierarchy": [],
    }),
  };
}

function updateDataset(state, event) {
  state.datasets = {
    ...state.datasets,
    [event.id]: Object.freeze({
      ...state.datasets[event.id],
      "metadata": event.data.metadata,
      "loaded": true,
      "mappings": event.data.mappings,
      "hierarchy": event.data.hierarchy,
    }),
  };
}

function updateHierarchy(state) {
  // Collect hierarchy from all datasets.
  const edgesAsStr = new Set();
  for (const dataset of Object.values(state.datasets)) {
    for (const [source, type, target] of dataset.hierarchy) {
      const asStr = `${source};${type};${target}`;
      edgesAsStr.add(asStr);
    }
  }
  // In previous step we removed duplicities, so now
  // we can parse the data.
  const edges = [];
  edgesAsStr.forEach((edge) => {
    edges.push(edge.split(";"));
  });
  state.hierarchy = Object.freeze(edges);
  // Now we can collect nodes.
  const nodes = {};
  for (const edge of edges) {
    nodes[edge[0]] = {
      "id": edge[0],
    };
    nodes[edge[2]] = {
      "id": edge[2],
    };
  }
  state.nodes = Object.freeze(nodes);
}

function addLabels(state, labels) {
  state.labels = Object.freeze({
    ...state.labels,
    ...labels,
  });
}

async function addDatasetAction(context, event) {
  const id = `${event.collection}:${event.dataset}`;
  if (context.state.datasets[event.dataset]) {
    return;
  }
  context.commit(
    createDataset.name,
    { "id": id, "collection": event.collection, "dataset": event.dataset }
  );
  const data = await fetchDatasetHierarchy(event.collection, event.dataset);
  context.commit(updateDataset.name, { "id": id, "data": data });
  context.commit(updateHierarchy.name);
  await fetchLabelsForHierarchy(context, data.hierarchy);
}

async function fetchLabelsForHierarchy(context, hierarchy) {
  const newNodes = collectMissingLabels(context.state.labels, hierarchy);
  if (newNodes.size > 0) {
    const newLabels = await fetchLabels([...newNodes]);
    context.commit(addLabels.name, newLabels);
  }
}

function collectMissingLabels(labels, hierarchy) {
  const newNodes = new Set();
  hierarchy.forEach((edge) => {
    if (labels[edge[0]] === undefined) {
      newNodes.add(edge[0]);
    }
    if (labels[edge[2]] === undefined) {
      newNodes.add(edge[2]);
    }
  });
  return newNodes;
}

// function extractMapping(dataset) {
//   function convertMapping(mapping) {
//     return mapping.map((item) => item.wikidata);
//   }
//
//   return {
//     "title": convertMapping(dataset["mapping.title"]),
//     "keyword": convertMapping(dataset["mapping.keyword"]),
//     "description": convertMapping(dataset["mapping.description"]),
//   };
// }

// function updateSelectionAction(context, dataset) {
//   const url = dataset.url;
//   context.commit(updateSelection.name, url);
// }
