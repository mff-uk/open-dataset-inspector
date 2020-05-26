module.exports = (api) => {
  api.cache.using(() => process.env.NODE_ENV);

  const presets = [
    ["@babel/preset-env", {
      "targets": {
        "chrome": 41,
      },
      "useBuiltIns": "usage",
      "corejs": {
        "version": 3,
        "proposals": true,
      },
    }],
  ];

  const plugins = [];

  const ignore = [
    // TypeScript and others may lure into node_modules and cause issues.
    // E.g.:
    // es.global-this.js:6 Uncaught TypeError: $ is not a function
    //     at Object../node_modules/core-js/modules/es.global-this.js
    "node_modules",
  ];

  return {
    "presets": presets,
    "plugins": plugins,
    "ignore": ignore,
  };
};
