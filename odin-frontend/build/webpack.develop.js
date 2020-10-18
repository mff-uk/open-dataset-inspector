const webpack = require("webpack");
const merge = require("webpack-merge");
const common = require("./webpack.common");

module.exports = merge(common, {
  "mode": "development",
  "devtool": "inline-source-map",
  "entry": [
    "webpack-hot-middleware/client",
  ],
  "devServer": {
    "hot": true,
  },
  "module": {
    "rules": [
      {
        // Apply linter during run development.
        "enforce": "pre",
        "test": /\.(js|vue)$/,
        "loader": "eslint-loader",
        "exclude": /node_modules/,
      },
      {
        "test": /\.css$/,
        "use": [
          "vue-style-loader",
          "css-loader",
        ],
      },
    ],
  },
  "plugins": [
    new webpack.HotModuleReplacementPlugin(),
  ],
});
