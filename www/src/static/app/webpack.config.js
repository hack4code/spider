const webpack = require("webpack");
const path = require("path");

const configuration = {};
const jspath = path.resolve(__dirname);

module.exports = {
    entry: {
        day: jspath + "/day.js",
        entries: jspath + "/entries.js",
        rss: jspath + "/rss.js",
        spiders: jspath + "/spiders.js"
    },

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
                    presets: [
                        '@babel/preset-env',
                        '@babel/preset-react',
                    ]
                },
            }
        ]
    },

    plugins: [
        new HtmlWebpackPlugin({
            title: 'Production',
        }),
    ],

   mode: 'development',
   devtool: 'inline-source-map',
};


/* vim: set ts=4 sw=4 sts=4 ft=javascript et: */
