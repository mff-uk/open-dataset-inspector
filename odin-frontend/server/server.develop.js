const express = require("express");
const webpack = require("webpack");
const path = require("path");
const webpackMiddleware = require("webpack-dev-middleware");
// https://github.com/webpack-contrib/webpack-hot-middleware
const webpackHotMiddleware = require("webpack-hot-middleware");
const webpackDevelop = require("../build/webpack.develop.js");
const server = require("./server.common");

(function initialize() {
  const app = express();
  server.initialize(app);
  initializeStatic(app);
  initializeWebpack(app);
  server.start(app);
}());

function initializeStatic(app) {
  const flagsPath = path.join(__dirname, "..", "public", "images");
  app.use("/images", express.static(flagsPath));
}

function initializeWebpack(app) {
  const webpackCompiler = webpack(webpackDevelop);
  app.use(webpackMiddleware(webpackCompiler, {
    "publicPath": webpackDevelop.output.publicPath.substr(1),
    "stats": {
      "colors": true,
      "chunks": false,
    },
  }));
  app.use(webpackHotMiddleware(webpackCompiler));
}
