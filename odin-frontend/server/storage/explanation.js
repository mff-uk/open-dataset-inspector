const path = require("path");
const fileSystem = require("fs");
const readline = require("readline");

const config = require("../configuration");
const { iriToFileName } = require("./dataset");
const { logger } = require("../logging");
const { fileToResponse, fileToJsonAsync, CONTENT_TYPE } = require("../utils");

let metadata = {};

(function initialize() {
  loadMetadata();
}());

function loadMetadata() {
  const filePath = path.join(config.data, "similarity-metadata.json");
  const readInterface = readline.createInterface({
    "input": fileSystem.createReadStream(filePath),
  });
  logger.info("Reading explanation metadata ...");
  let content = "";
  readInterface.on("line", (line) => {
    content += line;
  }).on("close", () => {
    metadata = JSON.parse(content).similarity;
    logger.info("Reading explanation metadata ... done",
      { "methods": Object.keys(metadata).length });
  });
}

function streamExplanation(response, similarityName, datasets) {
  const similarityMetadata = metadata[similarityName];
  if (similarityMetadata === undefined) {
    response.status(500).send({ "error": "Invalid similarity method." });
    return;
  }
  if (similarityMetadata.paired) {
    streamPairedExplanation(response, similarityName, datasets);
  } else {
    streamNonPairedExplanation(response, similarityName, datasets);
  }
}

function streamPairedExplanation(response, similarityName, datasets) {
  if (datasets.length !== 2) {
    response.status(500).send({ "error": "Expected two datasets." });
    return;
  }
  const names = datasets
    .map((iri) => iriToFileName(iri))
    .filter((name) => name !== undefined);
  names.sort();
  if (names.length !== 2) {
    response.status(500).send({ "error": "Can't find datasets." });
    return;
  }
  const filePath = path.join(
    config.data, "explanation", similarityName,
    `${names[0]}-${names[1]}.json`
  );
  fileToResponse(filePath, response, CONTENT_TYPE.JSON);
}

async function streamNonPairedExplanation(response, similarityName, datasets) {
  const paths = getDatasetFiles(similarityName, datasets);
  const result = {
    "datasets": datasets,
    "explanation": [],
  };
  await Promise.all(paths.map(
    (filePath) => fileToJsonAsync(filePath)
      .then((content) => result.explanation.push(content))
  ));
  response.json(result);
}

function getDatasetFiles(similarityName, queryDatasets) {
  return asArray(queryDatasets)
    .map((iri) => iriToFileName(iri))
    .filter((name) => name !== undefined)
    .map((name) => path.join(
      config.data, "explanation", similarityName, `${name}.json`
    ));
}

function asArray(value) {
  return Array.isArray(value) ? value : [value];
}

function streamMetadata(response) {
  response.json({
    "data": metadata,
  });
}

module.exports = {
  "streamExplanation": streamExplanation,
  "streamMetadata": streamMetadata,
};
