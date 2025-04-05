const webpack = require("webpack");
const HtmlWebpackPlugin = require('html-webpack-plugin');

const path = require("path");
const jspath = path.resolve(__dirname);

module.exports = {
    mode: 'production',
    entry: {
        day: jspath + "/day.js",
        entries: jspath + "/entries.js",
        rss: jspath + "/rss.js",
        spiders: jspath + "/spiders.js"
    },
    /* devtool: 'inline-source-map',*/
    /* plugins: [new HtmlWebpackPlugin({title: 'Development'})], */
    output: {
        path: jspath + "/../script/",
        filename: "[name].js",
        clean: true,
    },
    module: {
        rules: [
            {
                test: /\.js/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: {
                    presets: ['@babel/preset-env', '@babel/preset-react']
                }
            }
        ]
    }
};


/* vim: set ts=4 sw=4 sts=4 ft=javascript et: */
