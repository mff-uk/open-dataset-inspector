module.exports = {
  "root": true,
  "parserOptions": {
    "ecmaVersion": 9,
    "sourceType": "module",
  },
  "extends": [
    "airbnb/base",
    "plugin:vue/recommended"
  ],
  "rules": {
    "quotes": ["error", "double"],
    "indent": ["error", 2],
    "max-len": ["error", {
      "code": 80,
      "ignoreUrls": true,
      "ignoreRegExpLiterals": true,
    }],
    "curly": [2, "all"],
    "brace-style": ["error", "1tbs"],
    "semi": ["error", "always"],
    "comma-dangle": ["error", {
      "arrays": "always-multiline",
      "objects": "always-multiline",
      "imports": "always-multiline",
      "exports": "always-multiline",
    }],
    "object-shorthand": ["error", "never"],
    "quote-props": ["error", "always"],
    "no-use-before-define": ["error", "nofunc"],
    "prefer-destructuring": 0,
    "func-names": ["error", "as-needed"],
    "no-restricted-syntax": 0,
    "no-continue": 0,
    // Vuex modify params in the mutation functions.
    "no-param-reassign": ["error", {
      "props": true,
      "ignorePropertyModificationsFor": [
        "state"
      ]
    }]
  },
  "ignorePatterns": [ "client/similarity-visualisation" ]
};