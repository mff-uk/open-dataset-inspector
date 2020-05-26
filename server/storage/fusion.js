const csv = require("csv-parser");
const fileSystem = require("fs");

class FileNotFound extends Error {
  constructor() {
    super("File not found.");
    this.name = this.constructor.name;
  }
}

function maxFusion(iriFile, files) {
  const scores = [];
  const handler = (index, row) => {
    const oldScore = scores[index];
    const rowScore = safelyParseFloat(row.score);
    if (oldScore === undefined) {
      scores[index] = rowScore;
    } else {
      scores[index] = Math.max(oldScore, rowScore);
    }
  };
  return Promise.all(
    files.map((filePath) => iterateCsvFile(filePath, handler))
  ).then(() => scores);
}

function safelyParseFloat(value) {
  if (value === "inf") {
    return Number.MAX_SAFE_INTEGER;
  }
  return parseFloat(value);
}

function iterateCsvFile(filePath, handler) {
  return new Promise((resolve, reject) => {
    if (!fileSystem.existsSync(filePath)) {
      reject(new FileNotFound());
      return;
    }
    let cancelled = false;
    let index = 0;
    const stream = fileSystem.createReadStream(filePath)
      .pipe(csv())
      .on("data", (row) => {
        if (handler(index, row)) {
          // We do not need to read any more.
          stream.destroy();
          cancelled = true;
          resolve();
        }
        index += 1;
      })
      .on("end", () => {
        if (!cancelled) {
          resolve();
        }
      });
  });
}

function minFusion(iriFile, files) {
  const scores = [];
  const handler = (index, row) => {
    const oldScore = scores[index];
    const rowScore = safelyParseFloat(row.score);
    if (oldScore === undefined) {
      scores[index] = rowScore;
    } else {
      scores[index] = Math.min(oldScore, rowScore);
    }
  };
  return Promise.all(
    files.map((filePath) => iterateCsvFile(filePath, handler))
  ).then(() => scores);
}

module.exports = {
  "maxFusion": maxFusion,
  "minFusion": minFusion,
};
