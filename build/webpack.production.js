const merge = require("webpack-merge");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const common = require("./webpack.common");

module.exports = merge(common, {
  "mode": "production",
  "output": {
    "filename": "[name].[chunkhash].js",
  },
  "optimization": {
    "splitChunks": {
      "cacheGroups": {
        "commons": {
          "test": /[\\/]node_modules[\\/]/,
          "filename": "[name].[chunkhash].js",
          "name": "vendor",
          "chunks": "all",
        },
      },
    },
    "minimizer": [
      new OptimizeCSSAssetsPlugin({}),
      new TerserPlugin({
        "cache": true,
        "parallel": false,
        "sourceMap": false,
        "terserOptions": {
          "compress": {
            "ecma": 6,
          },
        },
      }),
    ],
  },
  "module": {
    "rules": [
      {
        "test": /\.css$/,
        "use": [
          MiniCssExtractPlugin.loader,
          "css-loader",
        ],
      },
    ],
  },
  "plugins": [
    new MiniCssExtractPlugin({
      "filename": "[name].[chunkhash].css",
    }),
  ],
});
