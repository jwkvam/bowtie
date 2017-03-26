const webpack = require('webpack');
// this is an ugly hack
const prod = process.argv.indexOf('--define') !== -1;
var path = require('path');
var CompressionPlugin = require('compression-webpack-plugin');


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
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                include: APP_DIR,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: [
                        ['latest', { 'modules': false}],
                        'react', 'stage-0'],
                    plugins: [
                        'transform-object-rest-spread',
                    ]
                }
            }, {
                test: /\.scss$/,
                loaders: ['style-loader', 'css-loader', 'sass-loader'],
            }, {
                test: /\.css$/,
                loader: 'style-loader!css-loader!sass-loader',
            }, {
                test: /\.less$/,
                loader: 'style-loader!css-loader!less-loader?strictMath&noIeCompat&',
            },
        ],
        noParse: [
            /plotly\.js$/
        ],
    },
    resolve: {
        extensions: ['.jsx', '.js', '.json'],
        modules: [
            path.resolve(__dirname, APP_DIR), 'node_modules'
        ]
    }
};

// for production
// https://github.com/webpack/webpack/issues/2537#issuecomment-250950677
if (prod) {
    config.devtool = 'cheap-module-source-map';
    config.plugins = [
        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false
        }),
        // https://facebook.github.io/react/docs/optimizing-performance.html
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('production')
        }),
        new webpack.optimize.UglifyJsPlugin({
            beautify: false,
            mangle: {
                screw_ie8: true,
                keep_fnames: false
            },
            compress: {
                warnings: false,
                booleans: true,
                screw_ie8: true,
                conditionals: true,
                loops: true,
                unused: true,
                comparisons: true,
                sequences: true,
                dead_code: true,
                evaluate: true,
                join_vars: true,
                if_return: true
            },
            comments: false,
        }),
        new CompressionPlugin({
            asset: '[path].gz[query]',
            algorithm: 'gzip',
        })
    ];
}

module.exports = config;
