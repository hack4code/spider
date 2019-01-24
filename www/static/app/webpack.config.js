const webpack = require("webpack");
const path = require("path");

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
      	    query: { presets:["react", "env", "stage-0"] }
	  }
      ]
  },

  plugins: [
      new webpack.DefinePlugin({
        "process.env": {
           NODE_ENV: JSON.stringify("production")
         }
      }),

      new webpack.optimize.minimize({
          compress: {
              warnings: false,
          },
          output: {
              comments: false,
          },
      }),
  ],
};
