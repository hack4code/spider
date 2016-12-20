var path = require("path");

var jspath = path.resolve(__dirname);

module.exports = {
  entry: {
    day: jspath + "/day.js",
    blog: jspath + "/blog.js",
    spentries: jspath + "/spentries.js",
    vote: jspath + "/vote.js",
    rss: jspath + "/rss.js",
    spider: jspath + "/spiders.js"
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
      	    query: { presets:["es2015", "react"]}
	  }
      ]
  }
};
