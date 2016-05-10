const path = require('path');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');

const HtmlWebpackPlugin = require('html-webpack-plugin');

const fs = require('fs');
const packageName = JSON.parse(fs.readFileSync('./package.json')).name;

const root = './' + packageName + '/angular2/';
const static = './' + packageName + '/static/angular2/';

console.log({root, static});
module.exports = {
  entry: {
    polyfills: [
      'reflect-metadata',
      'zone.js',
    ],
    vendor: [
      '@angular/core',
      '@angular/common',
      '@angular/compiler',
      '@angular/http',
      '@angular/platform-browser-dynamic',
      '@angular/platform-browser',
      'rxjs/Rx'
    ],
    main: root + '/src/main.ts'
  },
  output: {
    path: static,
    filename: '[name].bundle.js',
    sourceMapFilename: '[name].map',
    chunkFilename: '[id].chunk.js'
  },
  resolve: {
    root: [ path.join(root, 'src') ],
    extensions: ['', '.ts', '.js']
  },
  module: {
    loaders: [
      { test: /\.ts$/, loader: 'ts-loader', exclude: [/\.(spec|e2e)\.ts$/] },
      { test: /\.html$/, loader: 'raw-loader' },
      { test: /\.scss$/, loaders: ['raw-loader', 'postcss-loader', 'sass-loader'] }
    ],
    noParse: [
      path.join(root, 'node_modules', 'zone.js', 'dist'),
      path.join(root, 'node_modules', 'angular2', 'bundles')
    ]
  },
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(true),
    new webpack.optimize.CommonsChunkPlugin({name: ['vendor', 'polyfills'], minChunks: Infinity}),
    // new HtmlWebpackPlugin({
    //   template: static + './src/index.html',
    //   chunksSortMode: 'dependency' // will be removed in webpack2
    // })
  ],
  // thirdparty loader-configs
  postcss: function () {
    return [ autoprefixer ];
  }
};
