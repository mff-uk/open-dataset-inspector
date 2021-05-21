const fileSystem = require("fs");
const path = require("path");
const readline = require("readline");
const config = require("../configuration");
const { logger } = require("../logging");
const { fileToResponse, CONTENT_TYPE } = require("../utils");

let datasetIndex = {};

(function initialize() {
  loadDatasetIndex();
}());

function loadDatasetIndex() {
  const filePath = path.join(config.data, "dataset-metadata.json");
  const readInterface = readline.createInterface({
    "input": fileSystem.createReadStream(filePath),
  });
  logger.info("Reading dataset index ...");
  let content = "";
  readInterface.on("line", (line) => {
    content += line;
  }).on("close", () => {
    datasetIndex = JSON.parse(content).mapping;
    logger.info("Reading dataset index ... done",
      { "datasets": Object.keys(datasetIndex).length });
  });
}

function iriToFileName(iri) {
  return datasetIndex[iri];
}

function streamDataset(response, iri) {
  const fileName = iriToFileName(iri);
  const filePath = path.join(config.data, "dataset", `${fileName}.json`);
  fileToResponse(filePath, response, CONTENT_TYPE.JSON);
}

module.exports = {
  "iriToFileName": iriToFileName,
  "streamDataset": streamDataset,
};
