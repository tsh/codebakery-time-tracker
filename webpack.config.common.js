const path = require('path');

module.exports = {
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/static/',
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loaders: ['babel'],
        include: [path.join(__dirname, 'js')],
      },
      {
        test: /\.scss$/,
        loaders: ['style', 'css', 'sass'],
        include: [path.join(__dirname, 'scss')],
      },
      {
        test: /\.(png|woff|woff2|eot|ttf|svg)$/,
        loader: 'url-loader?limit=100000'
      }
    ],
  },
  sassLoader: {
    includePaths: [path.resolve(__dirname, 'node_modules/bootstrap/scss')],
  },
};
