var gulp           = require('gulp');
var tslint         = require('gulp-tslint');
var tslintStylish  = require('tslint-stylish');
var isCi           = require('is-ci');
var config         = require('../config').tslint;

/*
 * linting the TypeScript files using `codelyzer`.
 */

gulp.task('tslint', function () {
  return gulp.src(config.src)
    // .pipe(require('gulp-debug')())
    .pipe(tslint())
    .pipe(tslint.report(tslintStylish, {
      emitError: isCi,
      sort: true,
      bell: true
    }));
});
