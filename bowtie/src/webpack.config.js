var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var extractCSS = new ExtractTextPlugin('stylesheets/[name].css');
var extractLESS = new ExtractTextPlugin('stylesheets/[name].less');


var BUILD_DIR = path.resolve(__dirname, 'src/static');
var APP_DIR = path.resolve(__dirname, 'src/app');

var config = {
    entry: APP_DIR + '/index.jsx',
    output: {
        path: BUILD_DIR,
        filename: 'bundle.js'
    },
    module: {
        loaders: [
            {
                test: /\.jsx?/,
                include: APP_DIR,
                loader: 'babel',
                exclude: /nodemodules/,
                query: {
                    presets: ['es2015', 'react', 'stage-0'],
                    plugins: ['transform-object-rest-spread']
                }
            }, {
                test: /\.scss$/,
                loaders: ['style', 'css', 'sass'],
                exclude: /flexboxgrid/
            }, {
                test: /\.css$/,
                loader: extractCSS.extract(['css', 'sass']),
                exclude: /flexboxgrid/
            }, {
                test: /\.less$/,
                loader: extractLESS.extract(['less', 'sass']),
            }, {
                test: /\.(css|scss)$/,
                loader: 'style!css?modules',
                include: /flexboxgrid/
            }
        ],
        noParse: [
            /plotly\.js$/
        ]
    },
    plugins: [
        extractCSS,
        extractLESS,
    ],
    resolve: {
        extensions: ['', '.jsx', '.js', '.json'],
        modulesDirectories: [
            'node_modules',
            path.resolve(__dirname, './node_modules')
        ]

    }
};

if (process.env.NODE_ENV === 'production') {
    config.plugins.push(
        // https://facebook.github.io/react/docs/optimizing-performance.html
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                screw_ie8: true
            }
        })
    );
}

module.exports = config;
