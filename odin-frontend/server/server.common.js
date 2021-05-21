const bodyParser = require("body-parser");
const express = require("express");
const request = require("request");
const { logger } = require("./logging");
const config = require("./configuration");

const { streamDataset } = require("./storage/dataset");
const evaluation = require("./storage/evaluation");
const similarity = require("./storage/similarities");
const explanation = require("./storage/explanation");
const knowledge = require("./storage/knowledge");

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
    "/knowledge/:name/labels",
    bodyParser.json({ "limit": "16kb" }),
    (req, res) => knowledge.streamLabels(res, req.params.name, req.body)
  );
  router.get(
    "/evaluation/:group",
    (req, res) => evaluation.streamEvaluationGroup(res, req.params.group)
  );
  router.post(
    "/evaluation",
    bodyParser.json({ "limit": "64kb" }),
    evaluation.postEvaluation
  );
  router.get(
    "/similarity",
    (req, res) => explanation.streamMetadata(res)
  );
  router.get(
    "/similarity/explain/:similarity/",
    (req, res) => explanation.streamExplanation(
      res,
      req.params.similarity,
      req.query.dataset
    )
  );
  router.get(
    "/similarity/search/:similarity",
    (req, res) => similarity.streamSimilarToDataset(
      res,
      req.params.similarity,
      req.query.query,
      req.query.fusion || "min",
      parseInt(req.query.count || "7", 10)
    )
  );
  router.get(
    "/similarity/position/:similarity",
    (req, res) => similarity.streamPositionOfDatasets(
      res,
      req.params.similarity,
      req.query.query,
      req.query.dataset,
      req.query.fusion || "min"
    )
  );
  router.post(
    "/backend/graph-similarity",
    (req, res) => proxyToBackend("graph-similarity", req, res)
  );
  return router;
}

function proxyToBackend(path, req, res) {
  const url = `http://localhost:${config.backendPort}/${path}`;
  req.pipe(
    request.post(url, { "form": req.body }),
    { "end": false }
  ).pipe(res);
}

function start(app) {
  const port = config.frontendPort;
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
