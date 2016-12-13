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
    entry: APP_DIR + '/index',
    output: {
        path: BUILD_DIR,
        filename: 'bundle.js'
    },
    target: 'web',
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
            {
                test: /\.(js|jsx)$/,
                include: /nodemodules/,
                exclude: APP_DIR,
                loader: 'babel-loader',
                query: {
                    presets: ['react']
                }
            }, {
                test: /\.(js|jsx)$/,
                include: APP_DIR,
                loader: 'babel-loader',
                exclude: /nodemodules/,
                query: {
                    presets: [
                        ['es2015', { 'modules': false}],
                        'react', 'stage-0'],
                    plugins: ['transform-object-rest-spread']
                }
            }, {
                test: /\.scss$/,
// <<<<<<< HEAD
//                 loaders: ['style', 'css', 'sass'],
//             }, {
//                 test: /\.css$/,
//                 loader: extractCSS.extract(['css', 'sass']),
//             }, {
//                 test: /\.less$/,
//                 loader: extractLESS.extract(['less', 'sass']),
// =======
                loaders: ['style-loader', 'css-loader', 'sass-loader'],
            }, {
                test: /\.css$/,
                // loader: extractCSS.extract(['css-loader', 'sass-loader']),
                // loader: extractCSS.extract(['css-loader', 'sass-loader']),
                loader: "style-loader!css-loader!sass-loader",
            }, {
                test: /\.less$/,
                loader: "style-loader!css-loader!less-loader?strictMath&noIeCompat&"
                // loader: extractLESS.extract(['less-loader', 'sass-loader']),
            }, {
                include: /node_modules\/mapbox-gl-shaders/,
                enforce: 'post',
                loader: 'transform-loader',
                query: 'brfs'
// >>>>>>> webpack2 experiments
            }
        ],
        noParse: [
            /plotly\.js$/
        ]
    },
    // plugins: [
    //     extractCSS,
    //     extractLESS,
    // ],
    resolve: {
        extensions: ['.jsx', '.js', '.json'], //, '.web.js'],
        // modules: [ root('node_modules') ],
        // moduleExtensions: ['-loader'],
        // aliasFields: ['browser', 'index']
        // enforceExtension: true,
        // modules: [
        //     path.resolve(__dirname, "app"), "node_modules"
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
