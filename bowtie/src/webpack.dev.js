const merge = require('webpack-merge')
const common = require('./webpack.common.js')
var CompressionPlugin = require('compression-webpack-plugin');

var config = {
    mode: 'development'
}

module.exports = merge(common, config);
