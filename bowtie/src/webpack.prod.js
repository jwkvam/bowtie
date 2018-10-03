const merge = require('webpack-merge');
const common = require('./webpack.common.js');
var CompressionPlugin = require('compression-webpack-plugin');

var config = {
    mode: 'production',
    plugins: [
        new CompressionPlugin({
            filename: '[path].gz[query]',
            algorithm: 'gzip',
        })
    ]
};

module.exports = merge(common, config);
