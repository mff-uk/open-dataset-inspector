const fs = require("fs");
const path = require("path");
const readline = require("readline");
const config = require("../configuration");
const { logger } = require("../logging");

const wikidataLabels = {};

(function initialize() {
  loadAllLabels();
}());

function loadAllLabels() {
  const filePath = path.join(
    config.data, "www.wikidata.org", "wikidata-labels-en.jsonl"
  );
  const readInterface = readline.createInterface({
    "input": fs.createReadStream(filePath),
  });
  logger.info("Reading labels ...");
  readInterface.on("line", (line) => {
    const entity = JSON.parse(line);
    if (entity.label) {
      wikidataLabels[entity.id] = entity.label;
    }
  }).on("close", () => {
    logger.info("Reading labels ... done");
  });
}

/**
 * Return labels for given entities.
 */
function entitiesToLabel(response, entities) {
  const result = [];
  entities.forEach((id) => {
    result.push({
      "id": id,
      "label": wikidataLabels[id],
    });
  });
  response.status(200);
  response.json({
    "data": {
      "labels": result,
    },
  });
}

module.exports = {
  "entitiesToLabel": entitiesToLabel,
};
