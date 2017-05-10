const webpack = require("webpack");
const path = require("path");
const PrepackWebpackPlugin = require('prepack-webpack-plugin');

const configuration = {};
const jspath = path.resolve(__dirname);

module.exports = {
  entry: {
    day: jspath + "/day.js",
    blog: jspath + "/blog.js",
    entries: jspath + "/entries.js",
    vote: jspath + "/vote.js",
    rss: jspath + "/rss.js",
    spiders: jspath + "/spiders.js"
  },

  output: {
    path: jspath + "/js/",
    filename: "[name].js",
  },

  module: {
      loaders: [
          { test: /\.js/,
	    loader: "babel-loader",
	    exclude: /node_modules/,
      	    query: { presets:["react", "es2015", "stage-0"] }
	  }
      ]
  },

  plugins: [
  /*
      new webpack.ProvidePlugin({$: "jquery", jQuery: "jquery", "window.jQuery": "jquery"}),
  */
      new PrepackWebpackPlugin(configuration),

      new webpack.DefinePlugin({
        "process.env": {
           NODE_ENV: JSON.stringify("production")
         }
      }),

      new webpack.optimize.UglifyJsPlugin({
          compress: {
              warnings: false,
          },
          output: {
              comments: false,
          },
      }),
  ],
};
