import Vue from "vue";
import {
  fetchDatasetHierarchy,
  fetchLabels,
  fetchSimilarity,
} from "./visualisation-api.ts";
import {
  createDefaultPathOptions,
} from "./visualisation-service.ts";

export const STORE = "hierarchy";

const ADD_DATASET_ACTION = "add_dataset";
export const ADD_DATASET = `${STORE}/${ADD_DATASET_ACTION}`;

const REMOVE_DATASET_ACTION = "remove_dataset";
export const REMOVE_DATASET = `${STORE}/${REMOVE_DATASET_ACTION}`;

const SET_MAPPING_OPTIONS_ACTION = "set_mapping_filter";
export const SET_MAPPING_OPTIONS = `${STORE}/${SET_MAPPING_OPTIONS_ACTION}`;

const SET_SIMILARITY_OPTIONS_ACTION = "set_similarity_options";
// eslint-disable-next-line operator-linebreak
export const SET_SIMILARITY_OPTIONS =
  `${STORE}/${SET_SIMILARITY_OPTIONS_ACTION}`;

const FETCH_SIMILARITY_ACTION = "fetch_paths";
export const FETCH_SIMILARITY = `${STORE}/${FETCH_SIMILARITY_ACTION}`;

export const GET_DATASETS = "get_datasets";

export const GET_LABELS = "get_labels";

export const GET_NODES = "get_nodes";

export const GET_EDGES = "get_edges";

export const GET_HIERARCHY = "get_hierarchy";

export const GET_NODES_PROPERTIES = "get_nodes_props";

export const GET_SIMILARITY_AVAILABLE = "get_similarity_paths_available";

export const GET_SIMILARITY_PATHS = "get_similarity_paths";

export const GET_SIMILARITY_OPTIONS = "get_similarity_options";

export function createStore() {
  return {
    "namespaced": true,
    "state": {
      // Datasets as originally fetched.
      "datasets": {},
      // Datasets after application of mapping filters.
      "filteredDatasets": {},
      // Hierarchy data.
      "nodes": {},
      "hierarchy": [],
      // Nodes metadata
      "labels": {},
      "nodesProperties": {},
      // Filters for mappings, used to create 'filteredDatasets'.
      "mappingFilter": (mappings) => mappings,
      // Similarity as fetched, is connected to selected datasets.
      "similarity": emptySimilarity(),
      // Path options used for auto-fetch.
      "similarityOptions": createDefaultPathOptions(),
    },
    "mutations": {
      [createDataset.name]: createDataset,
      [updateDataset.name]: updateDataset,
      [deleteDataset.name]: deleteDataset,
      [rebuildHierarchy.name]: rebuildHierarchy,
      [addLabels.name]: addLabels,
      [rebuildNodesProperties.name]: rebuildNodesProperties,
      [setMappingOptions.name]: setMappingOptions,
      [clearSimilarity.name]: clearSimilarity,
      [setSimilarity.name]: setSimilarity,
      [setSimilarityLoading.name]: setSimilarityLoading,
      [setSimilarityOptions.name]: setSimilarityOptions,
    },
    "getters": {
      [GET_DATASETS]: (state) => Object.values(state.filteredDatasets),
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
      [GET_NODES_PROPERTIES]: (state) => state.nodesProperties,
      [GET_SIMILARITY_AVAILABLE]: (state) => state.similarity.fetched,
      [GET_SIMILARITY_PATHS]: (state) => state.similarity.data.paths,
      [GET_SIMILARITY_OPTIONS]: (state) => state.similarityOptions,
    },
    "actions": {
      [ADD_DATASET_ACTION]: addDatasetAction,
      [REMOVE_DATASET_ACTION]: removeDatasetAction,
      [SET_MAPPING_OPTIONS_ACTION]: setMappingOptionAction,
      [SET_SIMILARITY_OPTIONS_ACTION]: setSimilarityOptionsAction,
      [FETCH_SIMILARITY_ACTION]: fetchSimilarityAction,
    },
  };
}

/**
 * Not-fetched empty similarity record. Used so we do not need to check for
 * undefined.
 */
function emptySimilarity() {
  return {
    "fetched": false,
    "loading": false,
    "data": {},
    "datasets": [],
  };
}

function createDataset(state, event) {
  // We create an empty record, so we can use
  // it in the UI before the datasets is loaded.
  const dataset = Object.freeze({
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
  });
  state.datasets = {
    ...state.datasets,
    [event.id]: dataset,
  };
  state.filteredDatasets = {
    ...state.filteredDatasets,
    [event.id]: dataset,
  };
}

function updateDataset(state, event) {
  const dataset = Object.freeze({
    ...state.datasets[event.id],
    "metadata": event.data.metadata,
    "loaded": true,
    "mappings": event.data.mappings,
    "hierarchy": event.data.hierarchy,
  });
  state.datasets = {
    ...state.datasets,
    [event.id]: dataset,
  };
  state.filteredDatasets = {
    ...state.filteredDatasets,
    [event.id]: Object.freeze({
      ...dataset,
      "mappings": state.mappingFilter(event.data.mappings),
    }),
  };
}

function deleteDataset(state, event) {
  Vue.delete(state.datasets, event.id);
  Vue.delete(state.filteredDatasets, event.id);
}

function rebuildHierarchy(state) {
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

/**
 * Node properties are build from filtered 'filteredDatasets'.
 */
function rebuildNodesProperties(state) {
  const result = {};
  for (const id of Object.keys(state.nodes)) {
    result[id] = {
      "mappedBy": new Set(),
      "reducedFrom": new Set(),
      "mappingsMetadata": [],
      "directlyMapped": false,
    };
  }
  for (const dataset of Object.values(state.filteredDatasets)) {
    for (const mappings of dataset.mappings) {
      for (const mapping of mappings.data) {
        const node = result[mapping.id];
        if (node === undefined) {
          console.warn("Missing node ", mapping.id, " for mapping", mapping);
          continue;
        }
        const metadata = mapping.metadata;
        for (const token of (metadata.group || [])) {
          node.mappedBy.add(token);
        }
        for (const token of (metadata.reduced_from || [])) {
          node.reducedFrom.add(token);
        }
        node.mappingsMetadata.push(metadata);
        node.directlyMapped = node.directlyMapped || metadata.directly_mapped;
      }
    }
  }
  state.nodesProperties = Object.freeze(result);
}

function setMappingOptions(state, event) {
  state.mappingFilter = event;
  // Update datasets.
  const datasets = {};
  for (const [id, dataset] of Object.entries(state.datasets)) {
    datasets[id] = Object.freeze({
      ...dataset,
      "mappings": state.mappingFilter(dataset.mappings),
    });
  }
  state.filteredDatasets = datasets;
}

function clearSimilarity(state) {
  state.similarity = emptySimilarity();
}

function setSimilarity(state, event) {
  state.similarity = {
    "fetched": true,
    "loading": false,
    "data": event.similarity,
    "datasets": event.datasets,
  };
}

function setSimilarityLoading(state, event) {
  state.similarity.loading = event;
}

function setSimilarityOptions(state, event) {
  // TODO Check for change in option not delete options unless necessary.
  state.similarity = emptySimilarity();
  state.similarityOptions = event;
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
  context.commit(rebuildHierarchy.name);
  context.commit(rebuildNodesProperties.name);
  context.commit(clearSimilarity.name);
  await fetchLabelsForHierarchy(context, data.hierarchy);
  // We may need to fetch similarity if we have two datasets.
  if (Object.values(context.state.datasets).length === 2
    && context.state.similarityOptions.autoFetch) {
    const datasets = Object.values(context.state.filteredDatasets);
    if (datasets[0].loaded && datasets[1].loaded) {
      await context.dispatch(
        FETCH_SIMILARITY_ACTION,
        { "datasets": [datasets[0], datasets[1]] }
      );
    }
  }
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

function removeDatasetAction(context, event) {
  const id = `${event.collection}:${event.url}`;
  context.commit(deleteDataset.name, { "id": id });
  context.commit(rebuildHierarchy.name);
  context.commit(rebuildNodesProperties.name);
  context.commit(clearSimilarity.name);
}

function setMappingOptionAction(context, event) {
  context.commit(setMappingOptions.name, event);
  context.commit(rebuildNodesProperties.name);
  context.commit(clearSimilarity.name);
}

function setSimilarityOptionsAction(context, event) {
  context.commit(setSimilarityOptions.name, event);
  // TODO Make optional if there is no change to data.
  context.commit(clearSimilarity.name);
}

async function fetchSimilarityAction(context, event) {
  if (context.state.similarity.loading) {
    console.log("Already loading ...");
    return;
  }
  context.commit(setSimilarityLoading.name, true);
  let content;
  try {
    content = await fetchSimilarity(
      {
        ...context.state.similarityOptions,
        "autoFetch": undefined,
      },
      event.datasets[0], event.datasets[1]
    );
  } catch (error) {
    context.commit(setSimilarityLoading.name, false);
    throw error;
  }
  context.commit(setSimilarity.name, {
    "similarity": content,
    "datasets": [event.datasets[0].url, event.datasets[1].url],
  });
}
