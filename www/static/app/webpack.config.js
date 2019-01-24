const webpack = require("webpack");
const path = require("path");
const UglifyJsPlugin=require('uglifyjs-webpack-plugin');

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
      rules: [
          { test: /\.js/,
	    exclude: /node_modules/,
	    loader: "babel-loader",

	    options: {
                presets: [
                    '@babel/preset-env',
		    '@babel/preset-react',
                    {
                        plugins: [
                          '@babel/plugin-proposal-class-properties'
                        ]
                    }
               ]
	    },
	  }
      ]
  },

  plugins: [
      new webpack.DefinePlugin({
        "process.env": {
           NODE_ENV: JSON.stringify("production")
         }
      }),
  ],

  optimization: {
      minimizer: [
            new UglifyJsPlugin({
                uglifyOptions: {
                    compress: false
                }
            })
        ]
    },
};
