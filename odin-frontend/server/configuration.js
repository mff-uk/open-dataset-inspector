const fs = require("fs");
const path = require("path");
const YAML = require("yaml");

const file = path.join(__dirname, "..", "..", "config.yaml");
const content = fs.readFileSync(file, "utf8");
const configuration = YAML.parse(content).configuration;

// Update paths so it is relative from this directory.
configuration.data = path.join(__dirname, "..", "..", configuration.data);

module.exports = configuration;
