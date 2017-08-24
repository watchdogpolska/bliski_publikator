const fs = require('fs');
const path = require('path');
const webpack = require('webpack');

const packageName = JSON.parse(fs.readFileSync('./package.json')).name;
const root = path.resolve('./' + packageName + '/');
const source = path.join(root, 'angular2', 'src');
const static = path.join(root, 'static', 'angular2');

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
      '@angular/platform-browser-dynamic',
      '@angular/platform-browser',
      'ng2-dragula',
      'ngx-bootstrap',
      'rxjs',
    ],
    main: source + '/main.ts'
  },
  output: {
    path: static,
    filename: '[name].bundle.js',
    sourceMapFilename: '[name].map',
    chunkFilename: '[id].chunk.js'
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  module: {
    loaders: [
      // See https://github.com/TypeStrong/ts-loader/issues/572
      { test: /\.ts$/, loader: 'ts-loader?silent', exclude: [/\.(spec|e2e)\.ts$/] },
      { test: /\.html$/, loader: 'raw-loader' },
    ],
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: ['vendor', 'polyfills'],
      minChunks: Infinity
    }),
    new webpack.ContextReplacementPlugin(
      /angular(\\|\/)core(\\|\/)@angular/,
      path.resolve(__dirname, '../src')
    ),
  ],
};
