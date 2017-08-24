const fs = require('fs');
const path = require('path');

const webpack = require('webpack');
const webpackMerge = require('webpack-merge');
const commonConfig = require('./webpack.common.js');

const CleanWebpackPlugin = require('clean-webpack-plugin')

const packageName = JSON.parse(fs.readFileSync('./package.json')).name;
const root = path.resolve('./' + packageName + '/');
const source = path.join(root, 'angular2', 'src');
const static = path.join(root, 'static', 'angular2');

module.exports = webpackMerge(commonConfig, {
  cache: true,
  devtool: 'cheap-eval-source-map',
  entry: {
    polyfills: [
      'zone.js/dist/long-stack-trace-zone'
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      ENV: JSON.stringify('dev')
    }),
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.LoaderOptionsPlugin({
      debug: true
    }),
    new CleanWebpackPlugin([static], {dry: true, root: root})
  ]
});
