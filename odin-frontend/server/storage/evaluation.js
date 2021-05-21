const path = require("path");
const config = require("../configuration");
const { fileToResponse, jsonToFile, CONTENT_TYPE } = require("../utils");
const { logger } = require("../logging");

function streamEvaluationGroup(response, name) {
  const filePath = path.join(config.data, "evaluation", `${name}.json`);
  fileToResponse(filePath, response, CONTENT_TYPE.JSON);
}

function postEvaluation(request, response) {
  const task = request.body.task;
  let filePath;
  try {
    const time = (new Date()).getTime();
    const fileName = `${time}-${task.session}-${task.index}.json`;
    filePath = path.join(config.data, "evaluation", "report", fileName);
  } catch (error) {
    logger.error("Invalid data.", { "error": error });
    response.status(500).send("");
    return;
  }
  jsonToFile(request.body, filePath)
    .then(() => response.status(200).send(""))
    .catch((error) => {
      logger.error("Can't save report.", { "error": error });
      response.status(500).send("");
    });
}

module.exports = {
  "streamEvaluationGroup": streamEvaluationGroup,
  "postEvaluation": postEvaluation,
};
