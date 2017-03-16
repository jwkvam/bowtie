const webpack = require('webpack');
const prod = process.argv.indexOf('-p') !== -1;
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

// var extractCSS = new ExtractTextPlugin('stylesheets/[name].css');
// var extractLESS = new ExtractTextPlugin('stylesheets/[name].less');


function root(__path = '.') {
    return path.join(__dirname, __path);
}

var BUILD_DIR = path.resolve(__dirname, 'src/static');
var APP_DIR = path.resolve(__dirname, 'src/app');

var config = {
    // context: path.resolve(__dirname, './src'),
    context: __dirname,
    entry: APP_DIR + '/index.jsx',
    output: {
        path: BUILD_DIR,
        filename: 'bundle.js'
    },
    target: 'web',
    node: {
        fs: "empty"
    },
    module: {
        rules: [
            // {
            //     test: /\.(js|jsx)$/,
            //     include: APP_DIR,
            //     loader: 'babel-loader',
            //     // exclude: /nodemodules/,
            //     query: {
            //         presets: [
            //             ['es2015', { 'modules': false}],
            //             'react', 'stage-0'],
            //         plugins: ['transform-object-rest-spread']
            //     }
            //     test: /\.(js|jsx)$/,
            //     include: /node_modules/,
            //     exclude: APP_DIR,
            //     loader: 'babel-loader',
            //     query: {
            //         presets: ['react']
            //     }
            // }, {
            // {
            //     // test:
            //     test: /\.(js|jsx)$/,
            //     include: /glslify/,
            //     loader: "transform-loader?glslify",
            //     enforce: "post",
            // },
            {
            //     test: /\.js$/,
            //     include: /node_modules/,
            //     loader: "transform-loader",
            //     // enforce: "post"
            // }, {
            //     test: /\.js$/,
            //     include: /node_modules/,
            //     loader: "transform-loader?brfs",
            //     enforce: "post"
            // }, {
                test: /\.(js|jsx)$/,
                include: APP_DIR,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: [
                        ['es2015', { 'modules': false}],
                        'react', 'stage-0'],
                    plugins: [
                        'transform-object-rest-spread',
                        // 'babel-import-plugin'
                    ]
                }
            }, {
                test: /\.scss$/,
                loaders: ['style-loader', 'css-loader', 'sass-loader'],
            }, {
                test: /\.css$/,
                loader: "style-loader!css-loader!sass-loader",
            }, {
                test: /\.less$/,
                loader: "style-loader!css-loader!less-loader?strictMath&noIeCompat&",
                // loader: extractLESS.extract(['less-loader', 'sass-loader']),
            // }, {
            //     test: /\.(js|jsx)$/,
            //     include: /node_modules/,
            //     // enforce: 'post',
            //     loader: 'transform-loader/cacheable?brfs'
            // }, {
            //     loader: "transform-loader?brfs",
            //     enforce: "post"
            // }, {
            //     test: /\.(glsl|frag|vert)$/,
            //     loader: "transform-loader/cacheable?glslify",
            },
        ],
        noParse: [
            /plotly\.js$/
        ],
    },
    plugins: [
        new webpack.LoaderOptionsPlugin({
            options: {
                transforms: [
                    function(file) {
                        return through(function(buf) {
                            this.queue(buf.split("").map(function(s) {
                                return String.fromCharCode(127-s.charCodeAt(0));
                            }).join(""));
                        }, function() { this.queue(null); });
                    }
                ]
            }
        })
    //     extractCSS,
    //     extractLESS,
    ],
    resolve: {
        extensions: ['.jsx', '.js', '.json'], //, '.web.js'],
        // modules: [ root('node_modules') ],
        // moduleExtensions: ['-loader'],
        // aliasFields: ['browser', 'index']
        // enforceExtension: true,
        modules: [
            path.resolve(__dirname, APP_DIR), "node_modules"
        ]
        //     // 'node_modules',
        //     // 'src',
        //     // path.resolve(__dirname, 'src'),
        //     // path.resolve(__dirname, './node_modules')
        // ]
    }
};

// for production
// https://github.com/webpack/webpack/issues/2537#issuecomment-250950677
if (prod) {
    config.plugins.push(
        // https://facebook.github.io/react/docs/optimizing-performance.html
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        })
    );
}

module.exports = config;
