const webpack = require('webpack');
const webpackConfigCommon = require('./webpack.config.common.js');

module.exports = Object.assign({}, webpackConfigCommon, {
  devtool: 'eval',
  entry: [
    'react-hot-loader/patch',
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/only-dev-server',
    './js/index',
    './scss/index.scss',
  ],
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
  ],
});
