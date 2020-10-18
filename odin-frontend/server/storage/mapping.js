const path = require("path");
const fs = require("fs");

const config = require("../configuration");
const { iriToFileName } = require("./dataset");
const { fileToResponse } = require("../utils");

let collectionIndex = [];

(function initialize() {
  loadCollectionIndex();
}());

function loadCollectionIndex() {
  collectionIndex = fs.readdirSync(
    path.join(config.data, "mapping"),
    { "withFileTypes": true }
  )
    .filter((item) => item.isDirectory())
    .map((item) => item.name);
}

function streamMappingDataset(response, collection, dataset) {
  const fileName = iriToFileName(dataset);
  const filePath = path.join(
    config.data, "mapping", collection, `${fileName}.json`
  );
  fileToResponse(filePath, response, "application/json");
}

function streamMappingCollections(response) {
  response.json(collectionIndex);
}

module.exports = {
  "streamMappingDataset": streamMappingDataset,
  "streamMappingCollections": streamMappingCollections,
};
