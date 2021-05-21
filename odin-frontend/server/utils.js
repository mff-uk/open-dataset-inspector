const fileSystem = require("fs");
const { logger } = require("./logging");

module.exports = {
  "streamToFile": streamToFile,
  "jsonToFile": jsonToFile,
  "fileToStream": fileToStream,
  "fileToJson": fileToJson,
  "fileToJsonAsync": fileToJsonAsync,
  "fileToResponse": fileToResponse,
  "mkDir": mkDir,
  "remove": removeFile,
  //
  "CONTENT_TYPE": {
    "JSON": "application/json",
  },
};

function streamToFile(stream, path) {
  const outputStream = fileSystem.createWriteStream(path);
  stream.pipe(outputStream);
}

function jsonToFile(json, path) {
  const data = JSON.stringify(json);
  return new Promise((resolve, reject) => {
    fileSystem.writeFile(path, data, callbackToPromise(resolve, reject));
  });
}

function fileToStream(path, stream) {
  const inputStream = fileSystem.createReadStream(path);
  inputStream.pipe(stream);
}

function fileToJson(path) {
  return JSON.parse(fileSystem.readFileSync(path, "utf8"));
}

function fileToJsonAsync(path) {
  return new Promise((resolve, reject) => {
    fileSystem.readFile(path, "utf8", (error, data) => {
      if (error) {
        reject(error);
      }
      resolve(JSON.parse(data));
    });
  });
}

function fileToResponse(path, response, type) {
  if (!fileSystem.existsSync(path)) {
    response.status(404).send();
    return;
  }
  fileSystem.stat(path, (error, stat) => {
    if (error) {
      logger.error("Can't get file stats.", error);
      response.status(500).send();
      return;
    }
    response.writeHead(200, {
      "Content-Type": type,
      "Content-Length": stat.size,
    });
    fileToStream(path, response);
  });
}

function mkDir(path) {
  if (!fileSystem.existsSync(path)) {
    fileSystem.mkdirSync(path);
  }
}

function removeFile(path) {
  return new Promise((resolve, reject) => {
    fileSystem.unlink(path, callbackToPromise(resolve, reject));
  });
}

function callbackToPromise(resolve, reject) {
  return (error) => {
    if (error) {
      reject(error);
    } else {
      resolve();
    }
  };
}
