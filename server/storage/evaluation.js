const path = require("path");
const config = require("../configuration");
const { fileToResponse } = require("../utils");

function streamEvaluationGroup(response, name) {
  const filePath = path.join(config.data, "evaluation", `${name}.json`);
  fileToResponse(filePath, response, "application/json");
}

module.exports = {
  "streamEvaluationGroup": streamEvaluationGroup,
};
