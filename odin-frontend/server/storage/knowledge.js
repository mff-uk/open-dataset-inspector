const fileSystem = require("fs");
const path = require("path");
const readline = require("readline");
const config = require("../configuration");
const { logger } = require("../logging");

const labels = {};

let metadata = {};

(async function initialize() {
  await loadMetadata();
  await loadLabels();
}());

async function loadMetadata() {
  const filePath = path.join(config.data, "knowledge-metadata.json");
  const readInterface = readline.createInterface({
    "input": fileSystem.createReadStream(filePath),
  });
  logger.info("Reading knowledge metadata ...");
  let content = "";
  return new Promise((resolve) => {
    readInterface.on("line", (line) => {
      content += line;
    }).on("close", () => {
      metadata = JSON.parse(content).knowledge;
      logger.info("Reading knowledge metadata ... done",
        { "knowledgeGraphs": Object.keys(metadata).length });
    });
    resolve();
  });
}

async function loadLabels() {
  return Promise.all(Object.keys(metadata).map((name) => {
    const filePath = path.join(
      config.data, "knowledge", `${name}.jsonl`
    );
    const readInterface = readline.createInterface({
      "input": fileSystem.createReadStream(filePath),
    });
    logger.info("Reading labels ...");
    return new Promise((resolve) => {
      readInterface.on("line", (line) => {
        const entity = JSON.parse(line);
        if (entity.label) {
          labels[entity.id] = entity.label;
        }
      }).on("close", () => {
        logger.info(
          "Reading labels ... done",
          { "labels": Object.keys(labels).length }
        );
        resolve();
      });
    });
  }));
}

/**
 * Return labels for given entities.
 */
function streamLabels(response, knowledgeName, entities) {
  const knowledge = labels[knowledgeName] || {};
  const result = [];
  entities.forEach((id) => {
    result.push({
      "id": id,
      "label": knowledge[id],
    });
  });
  response.status(200);
  response.json({
    "data": {
      "labels": result,
    },
  });
}

function streamMetadata(response) {
  response.json({
    "data": metadata,
  });
}

module.exports = {
  "streamLabels": streamLabels,
  "streamMetadata": streamMetadata,
};
