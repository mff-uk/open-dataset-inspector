const bodyParser = require("body-parser");
const express = require("express");
const path = require("path");
const request = require("request");
const { logger } = require("./logging");
const config = require("./configuration");

const { streamDataset } = require("./storage/dataset");
const { entitiesToLabel } = require("./storage/wikidata-labels");
const { streamEvaluationGroup } = require("./storage/evaluation");
const {
  streamSimilarToDataset,
  streamPositionOfDatasets,
} = require("./storage/similarities");
const {
  streamMappingDataset,
  streamMappingCollections,
} = require("./storage/mapping");

const { jsonToFile } = require("./utils");

function initializeHttp(app) {
  app.use("/api/v1", createHttpApi());
}

function createHttpApi() {
  const router = express.Router();
  router.get(
    "/dataset",
    (req, res) => streamDataset(res, req.query.dataset)
  );
  router.post(
    "/wikidata/labels",
    bodyParser.json(),
    (req, res) => entitiesToLabel(res, req.body)
  );
  router.get(
    "/evaluation/:group",
    (req, res) => streamEvaluationGroup(res, req.params.group)
  );
  router.get(
    "/similarity/similar/:similarity",
    (req, res) => streamSimilarToDataset(
      res,
      req.params.similarity,
      req.query.query,
      req.query.fusion || "min",
      parseInt(req.query.count || "7", 10)
    )
  );
  router.get(
    "/similarity/position/:similarity",
    (req, res) => streamPositionOfDatasets(
      res,
      req.params.similarity,
      req.query.query,
      req.query.dataset,
      req.query.fusion || "min"
    )
  );
  router.post(
    "/evaluation",
    bodyParser.json({ "limit": "64kb" }),
    onPostEvaluation
  );
  router.get(
    "/mapping/:collection",
    (req, res) => streamMappingDataset(
      res,
      req.params.collection,
      req.query.dataset
    )
  );
  router.get(
    "/mapping",
    (req, res) => streamMappingCollections(res)
  );
  // curl -X POST -F "dataset=@000001.json" -F "dataset=@000005.json"
  //  -F 'options={"method": "closest"}'
  //  localhost:8065/api/v1/mapping-similarity
  router.post(
    "/mapping-similarity",
    (req, res) => {
      const url = `http://localhost:${config.pathServicePort}/`;
      req.pipe(
        request.post(url, { "form": req.body }),
        { "end": false }
      ).pipe(res);
    }
  );
  return router;
}

function onPostEvaluation(req, res) {
  const task = req.body.task;
  let filePath;
  try {
    const time = (new Date()).getTime();
    const fileName = `${time}-${task.session}-${task.index}.json`;
    filePath = path.join(config.data, "evaluation-reports", fileName);
  } catch (error) {
    logger.error("Invalid data.", { "error": error });
    res.status(500).send("");
    return;
  }
  jsonToFile(req.body, filePath)
    .then(() => res.status(200).send(""))
    .catch((error) => {
      logger.error("Can't save report.", { "error": error });
      res.status(500).send("");
    });
}

function start(app) {
  const port = config.servicePort;
  app.listen(port, (error) => {
    if (error) {
      logger.error("Can't start HTTP server.", { "error": error });
    }
    logger.info("Starting HTTP server.", { "port": port });
  });
}

module.exports = {
  "initialize": initializeHttp,
  "start": start,
};
