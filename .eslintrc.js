module.exports = {
  env: {
    browser: true,       // enables browser globals (window, document, etc.)
    es2021: true,        // enables ES2021 syntax
    node: true,          // enables Node.js globals (require, process, etc.)
  },
  extends: [
    "eslint:recommended", // ESLint's built-in recommended rules
  ],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",  // use "commonjs" if you use require()
  },
  rules: {
    // 🔴 Errors
    "no-unused-vars": "error",       // flag unused variables
    "no-undef": "error",             // flag undefined variables

    // 🟡 Warnings
    "no-console": "warn",            // warn on console.log statements
    "eqeqeq": "warn",                // require === instead of ==

    // 🟢 Style (optional)
    "semi": ["error", "always"],     // require semicolons
    "quotes": ["error", "double"],   // require double quotes
    "indent": ["error", 2],          // 2-space indentation
  },
};
