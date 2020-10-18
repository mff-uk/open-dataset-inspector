const fs = require("fs");
const path = require("path");
const YAML = require("yaml");

const file = fs.readFileSync(path.join(__dirname, "..", "config.yaml"), "utf8");
module.exports = YAML.parse(file).configuration;
