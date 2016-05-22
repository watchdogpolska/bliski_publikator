var gulp       = require('gulp');
var inject     = require('gulp-inject');
var config     = require('../config').inject;


/*
 * Injects bundled files in production
 */


gulp.task('inject', function () {
  var source = gulp.src(config.assets, {read: false});

  source.pipe(require('gulp-debug')({ title: "inject:files:"} ));

  gulp.src(config.src)
    .pipe(inject(source, config.options))
    .pipe(gulp.dest(config.dest));
});
