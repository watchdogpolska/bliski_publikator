var bowerFiles  = require('main-bower-files');
var gulp   = require('gulp');
var gulpFilter  = require('gulp-filter');
var config = require('../config').fonts;

gulp.task('fonts', function(){
	var fontsFilter = gulpFilter(['**/*.{eot,svg,ttf,woff,woff2}']);

	return gulp.src(bowerFiles())
		.pipe(fontsFilter)
		.pipe(gulp.dest(config.dest));
})
