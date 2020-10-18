const path = require("path");
const webpack = require("webpack");
const { VueLoaderPlugin } = require("vue-loader");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  "entry": [
    path.join(__dirname, "..", "client", "index.js"),
  ],
  "output": {
    "path": path.join(__dirname, "..", "dist"),
    "filename": "bundle.js",
    "publicPath": "./",
  },
  "resolve": {
    "modules": ["node_modules"],
    "extensions": [".js", ".vue", ".ts"],
  },
  "module": {
    "rules": [
      {
        "test": /\.vue$/,
        "use": "vue-loader",
      }, {
        "test": /\.js$/,
        "use": "babel-loader",
      }, {
        "test": /\.ts$/,
        "loader": "ts-loader",
        // Allow use of lang="ts" in the vue file
        "options": { "appendTsSuffixTo": [/\.vue$/] },
      },
    ],
  },
  "plugins": [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({
      "filename": "index.html",
      "template": path.join(__dirname, "..", "public", "index.html"),
      "inject": true,
    }),
    new webpack.DefinePlugin({}),
  ],
};
