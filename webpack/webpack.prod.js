const webpackMerge = require('webpack-merge');
const commonConfig = require('./webpack.common.js');
const webpack = require('webpack');

const UglifyJSPlugin = require('uglifyjs-webpack-plugin')

module.exports = webpackMerge(commonConfig, {
  devtool: 'source-map',
  entry: {
    polyfills: [
      'es6-shim',
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      ENV: JSON.stringify('prod')
    }),
    new UglifyJSPlugin({
      beautify: false, //prod
      output: {
        comments: false
      }, //prod
      mangle: {
        screw_ie8: true
      }, //prod
      compress: {
        screw_ie8: true,
        warnings: false,
        conditionals: true,
        unused: true,
        comparisons: true,
        sequences: true,
        dead_code: true,
        evaluate: true,
        if_return: true,
        join_vars: true,
        negate_iife: false // we need this for lazy v8
      },
    }),
  ]
});
