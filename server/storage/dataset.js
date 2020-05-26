const fs = require("fs");
const path = require("path");
const readline = require("readline");
const config = require("../configuration");
const { logger } = require("../logging");
const { fileToResponse } = require("../utils");

let datasetIndex = {};

(function initialize() {
  loadDatasetIndex();
}());

function loadDatasetIndex() {
  const filePath = path.join(config.data, "dataset-iri-to-file-name.json");
  const readInterface = readline.createInterface({
    "input": fs.createReadStream(filePath),
  });
  logger.info("Reading dataset index ...");
  readInterface.on("line", (line) => {
    datasetIndex = JSON.parse(line);
  }).on("close", () => {
    logger.info("Reading dataset index ... done");
  });
}

function iriToFileName(iri) {
  return datasetIndex[iri];
}

function streamDataset(response, iri) {
  const fileName = iriToFileName(iri);
  const filePath = path.join(config.data, "datasets", `${fileName}.json`);
  fileToResponse(filePath, response, "application/json");
}

module.exports = {
  "iriToFileName": iriToFileName,
  "streamDataset": streamDataset,
};
