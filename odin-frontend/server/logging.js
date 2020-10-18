const winston = require("winston");

const MS_PER_SEC = 1e3;

const NS_PER_MS = 1e6;

let logger;

(function initialize() {
  logger = winston.createLogger({
    "level": "info",
    "format": winston.format.combine(
      winston.format.timestamp({
        "format": "YYYY-MM-DD'T'HH:mm:ss",
      }),
      winston.format.json()
    ),
    "transports": [
      new winston.transports.Console(),
    ],
  });

  // Do not exit after the uncaught exception.
  logger.exitOnError = false;

  module.exports = {
    "logger": logger,
    "measureTime": wrapCallbackWithTimeMeasure,
  };
}());

function wrapCallbackWithTimeMeasure(name, callback) {
  return function measureTime(...args) {
    const start = process.hrtime();
    callback(...args);
    const duration = process.hrtime(start);
    const durationInMs = Math.floor(
      (duration[0] * MS_PER_SEC) + (duration[1] / NS_PER_MS)
    );
    logger.info(name, { "duration": durationInMs });
  };
}
