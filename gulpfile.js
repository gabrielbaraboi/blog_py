var gulp         = require('gulp'),
		sass         = require('gulp-sass'),
		concat       = require('gulp-concat'),
		uglify       = require('gulp-uglify-es').default,
		cleancss     = require('gulp-clean-css'),
		autoprefixer = require('gulp-autoprefixer');

// Custom Styles
gulp.task('styles', function() {
	return gulp.src('resources/sass/**/*.sass')
	.pipe(sass({
		outputStyle: 'expanded',
		includePaths: [__dirname + '/node_modules']
	}))
	.pipe(concat('styles.min.css'))
	.pipe(autoprefixer({
		grid: true,
		overrideBrowserslist: ['last 10 versions']
	}))
	.pipe(cleancss( {level: { 1: { specialComments: 0 } } })) // Optional. Comment out when debugging
	.pipe(gulp.dest('static/css'))
});

// Scripts & JS Libraries
gulp.task('scripts', function() {
	return gulp.src([
		// 'node_modules/jquery/dist/jquery.min.js', // Optional jQuery plug-in (npm i --save-dev jquery)
		// 'resources/js/_libs.js', // JS libraries (all in one)
		'resources/js/custom.js', // Custom scripts. Always at the end
		])
	.pipe(concat('scripts.min.js'))
	.pipe(uglify()) // Minify js (opt.)
	.pipe(gulp.dest('static/js'))
});

gulp.task('watch', function() {
	gulp.watch('resources/sass/**/*.sass', gulp.parallel('styles'));
	gulp.watch('resources/js/custom.js', gulp.parallel('scripts'));
});

gulp.task('default', gulp.parallel('styles', 'scripts', 'watch'));
