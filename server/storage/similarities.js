//
// The "similarities" directory stores distance matrices.
//

const path = require("path");
const fileSystem = require("fs");
const csv = require("csv-parser");

const config = require("../configuration");
const { iriToFileName } = require("./dataset");
const { logger } = require("../logging");
const { minFusion, maxFusion } = require("./fusion");

const fusionMethods = {
  "min": minFusion,
  "max": maxFusion,
};

function streamSimilarToDataset(
  response, similarityName, queryDatasets, fusion, count
) {
  const fusionMethod = fusionMethods[fusion];
  if (fusionMethod === undefined) {
    response.status(500).send({ "error": "Invalid fusion method." });
    return;
  }
  const files = getDatasetFiles(similarityName, queryDatasets);
  if (files.length === 0) {
    response.status(500).send({ "error": "No valid dataset provided." });
    return;
  }
  const iriFile = getIriFile(similarityName);
  fusionMethod(iriFile, files)
    .then((distances) => loadIris(iriFile)
      .then((iris) => scoresToDatasets(iris, distances)))
    .then((datasets) => datasetsResponse(
      datasets, queryDatasets, count
    ))
    .then((content) => response.json(content))
    .catch((error) => {
      logger.error("Can't get similarities.", error);
      response.status(500).send();
    });
}

function getDatasetFiles(similarityName, queryDatasets) {
  return asArray(queryDatasets)
    .map((iri) => iriToFileName(iri))
    .filter((name) => name !== undefined)
    .map((name) => path.join(
      config.data, "similarities", similarityName, `${name}.csv`
    ));
}

function asArray(value) {
  return Array.isArray(value) ? value : [value];
}

function getIriFile(similarityName) {
  return path.join(config.data, "similarities", similarityName, "datasets.csv");
}

function loadIris(iriFile) {
  return new Promise((resolve) => {
    const result = [];
    fileSystem.createReadStream(iriFile)
      .pipe(csv())
      .on("data", (row) => {
        result.push(row.iri);
      })
      .on("end", () => {
        resolve(result);
      });
  });
}

function scoresToDatasets(iris, scores) {
  const datasets = [];
  for (const index in scores) {
    if (!Object.prototype.hasOwnProperty.call(scores, index)) {
      continue;
    }
    const iri = iris[index];
    const score = scores[index];
    datasets.push({
      "iri": iri,
      "score": score,
    });
  }
  // We sort in increasing order as the scores contain distance.
  datasets.sort((left, right) => -(right.score - left.score));
  return datasets;
}

function datasetsResponse(datasets, queryDatasets, count) {
  const resultDatasets = selectTopNDatasets(datasets, queryDatasets, count);
  const scoreThreshold = resultDatasets[resultDatasets.length - 1].score;
  let countWithThresholdValue = 0;
  for (let index = count + 1; index < datasets.length; index += 1) {
    if (datasets[index].score === scoreThreshold) {
      countWithThresholdValue += 1;
    } else {
      break;
    }
  }
  return {
    "query": {
      "datasets": queryDatasets,
    },
    "datasets": resultDatasets,
    "numDatasets": datasets.length,
    "numSameScoreAsLast": countWithThresholdValue,
  };
}

function selectTopNDatasets(datasets, toIgnore, size) {
  const result = [];
  for (const dataset of datasets) {
    if (toIgnore.includes(dataset.iri)) {
      continue;
    }
    result.push(dataset);
    if (result.length >= size) {
      return result;
    }
  }
  return result;
}

function streamPositionOfDatasets(
  response, similarityName, queryDatasets, searchedDatasets, fusion
) {
  if (searchedDatasets === undefined || searchedDatasets.length === 0) {
    response.json({ "datasets": [] });
    return;
  }
  const fusionMethod = fusionMethods[fusion];
  if (fusionMethod === undefined) {
    response.status(500).send({ "error": "Invalid fusion method." });
    return;
  }
  const files = getDatasetFiles(similarityName, queryDatasets);
  if (files.length === 0) {
    response.status(500).send({ "error": "No valid dataset provided." });
    return;
  }
  const iriFile = getIriFile(similarityName);
  fusionMethod(iriFile, files)
    .then((distances) => loadIris(iriFile)
      .then((iris) => scoresToDatasets(iris, distances)))
    .then((datasets) => positionOfDatasetsResponse(
      datasets, queryDatasets, searchedDatasets
    ))
    .then((content) => response.json(content))
    .catch((error) => {
      logger.error("Can't get similarities.", error);
      response.status(500).send();
    });
}

function positionOfDatasetsResponse(
  datasets, queryDatasets, searchedDatasets
) {
  const result = [];
  let lastScore;
  let lastScoreStart;
  let position = 0;
  for (const index in datasets) {
    if (!Object.prototype.hasOwnProperty.call(datasets, index)) {
      continue;
    }
    const iri = datasets[index].iri;
    if (queryDatasets.includes(iri)) {
      continue;
    }
    position += 1;
    const score = datasets[index].score;
    if (score !== lastScore) {
      // Assign position to all before.
      for (const item of result) {
        if (item.positionMax) {
          continue;
        }
        item.positionMax = position - 1;
      }
      //
      lastScore = score;
      lastScoreStart = position;
    }
    if (searchedDatasets.includes(iri)) {
      result.push({
        "iri": iri,
        "score": datasets[index].score,
        "positionMin": lastScoreStart,
      });
    }
  }
  // Assign position to all before.
  for (const item of result) {
    if (item.positionMax) {
      continue;
    }
    item.positionMax = datasets.length - 1;
  }
  return {
    "datasets": result,
    "numDatasets": datasets.length,
  };
}

module.exports = {
  "streamSimilarToDataset": streamSimilarToDataset,
  "streamPositionOfDatasets": streamPositionOfDatasets,
};
