var bowerFiles  = require('main-bower-files');
var gulp   = require('gulp');
var gulpFilter  = require('gulp-filter');
var config = require('../config').fonts;

gulp.task('fonts', function(){
	var fontsFilter = gulpFilter(['**/*.{eot,svg,ttf,woff,woff2}']);

	var stream = gulp.src(bowerFiles())
		.pipe(fontsFilter)

	config.dest.forEach(function(dest){
		stream.pipe(gulp.dest(dest));
	})
})
