const webpack = require('webpack');
const webpackConfigCommon = require('./webpack.config.common.js');

module.exports = Object.assign({}, webpackConfigCommon, {
  devtool: 'source-map',
  entry: [
    './js/index',
    './scss/entry.scss',
  ],
  plugins: [
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production'),
      },
    }),
    new webpack.optimize.UglifyJsPlugin({
      compressor: {
        warnings: false,
      },
    }),
  ],
});
