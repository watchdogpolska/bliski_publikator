var gulp        = require('gulp');
var bowerFiles  = require('main-bower-files');
var gulpFilter  = require('gulp-filter');
var concat      = require('gulp-concat');
var uglify      = require('gulp-uglify');
var cssnano     = require('gulp-cssnano');
var config      = require('../config');


gulp.task('optimize', function () {
  // creates stream of main bower files
  var files = bowerFiles();
  // project js and css files
  files = files.concat(config.scripts.src);
  files = files.concat(config.styles.src);

  // filters
  var mainFilter = gulpFilter(['**/*.js', '**/*.css']);
  var jsFilter = gulpFilter('**/*.js', {restore: true});
	var cssFilter = gulpFilter('**/*.css', {restore: true});

  return gulp.src(files)
    // gets rid of non .js or .css files
    .pipe(mainFilter)
    // work only on js
		.pipe(jsFilter)
    // concat js files (name of resulting file, options)
		.pipe(concat(config.optimize.js.fileName, config.optimize.js.concat))
    // uglify js
    .pipe(uglify(config.optimize.js.uglify))
    // restores files stream
		.pipe(jsFilter.restore)
    // work only on css
		.pipe(cssFilter)
    // concat css (name of resulting file, options)
    .pipe(concat(config.optimize.css.fileName, config.optimize.css.concat))
    // minify css (options)
    .pipe(cssnano(config.optimize.css.cssnano))
    // restores files stream
		.pipe(cssFilter.restore)
    // saves bundled files
		.pipe(gulp.dest(config.optimize.dest));
});
