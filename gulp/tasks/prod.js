var gulp = require('gulp');
var runSequence = require('run-sequence');


gulp.task('prod', function(callback){
  runSequence(
    'bower',
    'delete:prod',
    'deps',
    'fonts',
    'scripts',
    'styles',
    'optimize',
    'inject',
    'webpack:prod',
    callback
  );
});
