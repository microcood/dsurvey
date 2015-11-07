var gulp = require('gulp');
var sass = require('gulp-sass');
var livereload = require('gulp-livereload');

gulp.task('sass', function() {
  gulp.src('scss/app.scss')
    .pipe(sass())
    .pipe(gulp.dest('static/dist/css'))
    .pipe(livereload());
});

gulp.task('watch', function() {
  livereload.listen();
  gulp.watch('scss/**/*.scss', ['sass']);
});