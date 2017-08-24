var gulp = require('gulp');
var webpack = require('webpack');
var webpackStream = require('webpack-stream');
var gutil = require('gulp-util');
var config = require('../config').webpack;

gulp.task("webpack:dev", function(callback) {
  gutil.log("[webpack]", "Start webpack"); 
  webpack(
    require('../../webpack/webpack.dev'),
    function(err, stats) {
      if(err) throw new gutil.PluginError("webpack", err);
      gutil.log("[webpack]", "Compiled");
      callback();
  });
});

gulp.task("webpack:prod", function(callback) {
  gutil.log("[webpack]", "Start webpack");  
  webpack(
    require('../../webpack/webpack.prod'),
    function(err, stats) {
      if(err) throw new gutil.PluginError("webpack", err);
      gutil.log("[webpack]", "Compiled");
      callback();
  });
});

gulp.task("webpack", ["webpack:dev"]);
