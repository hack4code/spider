var webpack = require("webpack");
var path = require("path");
var jspath = path.resolve(__dirname);

module.exports = {
  entry: {
    day: jspath + "/day.js",
    blog: jspath + "/blog.js",
    spentries: jspath + "/spentries.js",
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
      new webpack.ProvidePlugin({$: "jquery", jQuery: "jquery", "window.jQuery": "jquery"}),
  ],
};
