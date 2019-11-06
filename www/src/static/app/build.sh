#! /usr/bin/env bash


npm init -f

npm install react --save-dev
npm install react-dom --save-dev
npm install whatwg-fetch --save-dev
npm install @babel/core --save-dev
npm install @babel/preset-env --save-dev
npm install @babel/preset-react --save-dev
npm install @babel/plugin-proposal-class-properties --save-dev
npm install babel-loader --save-dev
npm install webpack --save-dev
npm install webpack-cli --save-dev

node_modules/.bin/webpack --mode production --config webpack.config.js
