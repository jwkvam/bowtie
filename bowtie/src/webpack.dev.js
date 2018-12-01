const merge = require('webpack-merge');
const common = require('./webpack.common.js');

var config = {
    mode: 'development',
};

module.exports = merge(common, config);
