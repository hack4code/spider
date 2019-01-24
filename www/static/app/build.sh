#! /bin/bash

npm init -f

npm install react --save-dev
npm install react-dom --save-dev
npm install react-transition-group --save-dev
npm install whatwg-fetch --save-dev
# npm install prepack --save-dev
# npm install prepack-webpack-plugin --save-dev
# npm install jquery --save-dev
npm install @babel/core --save-dev
npm install babel-preset-env --save-dev
# npm install babel-preset-es2015 --save-dev
npm install babel-preset-react --save-dev
npm install babel-preset-stage-0 --save-dev
npm install uglifyjs-webpack-plugin --save-dev
npm install webpack --save-dev
npm install webpack-cli --save-dev
npm install babel-loader --save-dev
# npm install webpack-cli -g
# npm install webpack -g

node_modules/.bin/webpack --config webpack.config.js

