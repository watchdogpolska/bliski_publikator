var fs = require('fs');
var packageName       = JSON.parse(fs.readFileSync('./package.json')).name;

var srcAssets         = packageName + '/assets/';
var devStatic         = packageName + '/static/dev';
var prodStatic        = packageName + '/static/prod';

var srcTemplates      = packageName + '/templates';
var devTemplates      = packageName + '/templates_dev';
var prodTemplates     = packageName + '/templates_prod';

var baseTemplate      = srcTemplates + '/base.html';
var baseScss          = srcAssets + '/scss/style.scss';


var injectTransform = function (filepath, file, index, length, targetFile) {
  if (filepath.slice(-3) === '.js') {
      return '<script src="\{% static \''+ filepath +'\' %\}"></script>';
  } else if (filepath.slice(-4) === '.css') {
      return '<link rel="stylesheet" href="\{% static \'' + filepath + '\' %\}">';
  } else {
    return inject.transform.apply(inject.transform, arguments);
  }
};

module.exports = {
  browsersync: {
    dev: {
      port: 8000,
      ui: {
        port: 8080
      },
      proxy: 'localhost:8010',
      open: false,
      files: [
        devStatic + '/styles/*.css',
      ]
    }
  },
  delete: {
    dev: [devStatic, devTemplates],
    prod: [devStatic, prodStatic, prodTemplates]
  },
  deps: {
    src: baseTemplate,
    dest: devTemplates,
    bower: {
      options: {
        name: 'bower',
        addRootSlash: false,
        ignorePath: 'bower_components/',
        transform: injectTransform
      }
    },
    project: {
      assets: [devStatic + '/**/*.js', devStatic + '/**/*.css'],
      options: {
        addRootSlash: false,
        ignorePath: packageName + '/static/',
        transform: injectTransform
      }
    }
  },
  fonts: {
    dest: [
      prodStatic + '/fonts/',
      devStatic + '/fonts'
    ]
  },
  inject: {
    src: baseTemplate,
    dest: prodTemplates,
    assets: [prodStatic + '/**/*.js', prodStatic + '/**/*.css'],
    options: {
      addRootSlash: false,
      ignorePath: packageName + '/static/',
      transform: injectTransform
    }
  },
  optimize: {
    dest: prodStatic,
    mainBowerFiles: {},
    js:{
      src: devStatic + '/**/*.js',
      fileName: 'scripts/bundle.js',
      concat: {},
      uglify: {}
    },
    css: {
      src: devStatic + '/**/*.css',
      fileName: 'styles/bundle.css',
      concat: {},
      cssnano: {}
    }
  },
  scripts: {
    src: srcAssets + '/scripts/*.js',
    dest: devStatic + '/scripts'
  },
  styles: {
    src: baseScss,
    dest: devStatic + '/styles/',
    postcss: {
      autoprefixer: {
        browsers: [
          'last 2 versions',
          'safari 5',
          'ie 8',
          'ie 9',
          'opera 12.1',
          'ios 6',
          'android 4'
        ],
        cascade: true
      },
      mqpacker: {}
    },
    inject: {
      options: {
        relative: true
      }
    }
  },
  watch: {
    scss: srcAssets  + '/scss/*.scss',
    js: srcAssets + '/scripts/*.js',
    html: baseTemplate
  },
  webpack: {
    entry: packageName + '/angular2/src/main.ts',
    dev: {
      dest: devStatic + '/angular2/'
    },
    prod: {
      dest: prodStatic + '/angular2/'
    }
  }
};
