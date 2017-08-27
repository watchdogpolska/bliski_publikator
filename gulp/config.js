var fs = require('fs');
var packageName       = JSON.parse(fs.readFileSync('./package.json')).name;

var srcAssets         = packageName + '/assets/';
var destAssets        = packageName + '/static/assets/';

var srcTemplates      = packageName + '/main/templates';
var destTemplates     = packageName + '/main/templates_inject';

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
        destAssets + '/styles/*.css',
      ]
    }
  },
  delete: [destAssets, destTemplates],
  deps: {
    src: baseTemplate,
    dest: destTemplates,
    bower: {
      options: {
        name: 'bower',
        addRootSlash: false,
        ignorePath: 'bower_components/',
        transform: injectTransform
      }
    },
    project: {
      assets: [
        destAssets + '/**/*.js',
        destAssets + '/**/*.css'
      ],
      options: {
        addRootSlash: false,
        ignorePath: packageName + '/static/',
        transform: injectTransform
      }
    }
  },
  fonts: {
    dest: destAssets + '/fonts'
  },
  inject: {
    src: baseTemplate,
    dest: destTemplates,
    assets: [destAssets + '/**/*.js', destAssets + '/**/*.css'],
    options: {
      addRootSlash: false,
      ignorePath: packageName + '/static/',
      transform: injectTransform
    }
  },
  optimize: {
    dest: destAssets,
    mainBowerFiles: {},
    js:{
      fileName: 'scripts/bundle.js',
      concat: {},
      uglify: {}
    },
    css: {
      fileName: 'styles/bundle.css',
      concat: {},
      cssnano: {}
    }
  },
  scripts: {
    src: [ srcAssets + '/scripts/*.js' ],
    dest: destAssets + '/scripts'
  },
  styles: {
    src: [
      baseScss
    ],
    dest: destAssets + '/styles/',
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
  tslint: {
    src: [
      packageName + '/angular2/src/**/*.ts',
      '!' + packageName + '/angular2/src/**/*.d.ts'
    ]
  },
  watch: {
    scss: srcAssets  + '/scss/*.scss',
    js: srcAssets + '/scripts/*.js',
    html: baseTemplate
  },
};
