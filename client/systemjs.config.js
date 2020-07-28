(function (global) {
  // simplified version of Object.assign for es3
  function assign () {
    const result = {}
    for (let i = 0, len = arguments.length; i < len; i++) {
      const arg = arguments[i]
      for (const prop in arg) {
        result[prop] = arg[prop]
      }
    }
    return result
  }

  System.config({
    transpiler: 'plugin-babel',
    defaultExtension: 'js',
    paths:
            Object.assign(
              {
                // paths serve as alias
                'npm:': 'https://unpkg.com/'
              }, systemJsPaths
            ),
    map: assign(
      {
        // babel transpiler
        'plugin-babel': 'npm:systemjs-plugin-babel@0.0.25/plugin-babel.js',
        'systemjs-babel-build': 'npm:systemjs-plugin-babel@0.0.25/systemjs-babel-browser.js',

        // css plugin
        css: 'npm:systemjs-plugin-css/css.js',

        // vuejs
        vue: 'npm:vue/dist/vue.min.js',

        // vue property decorator
        'vue-class-component': 'npm:vue-class-component@6.3.2/dist/vue-class-component.min.js',
        'vue-property-decorator': 'npm:vue-property-decorator@7.2.0/lib/vue-property-decorator.umd.js',

        app: `${appLocation}app`
      },
      systemJsMap
    ), // systemJsMap comes from index.html

    packages: {
      vue: {
        defaultExtension: 'js'
      },
      'vue-class-component': {
        defaultExtension: 'js'
      },
      'vue-property-decorator': {
        defaultExtension: 'js'
      },
      app: {
        defaultExtension: 'js'
      },
      '@ag-grid-community/vue': {
        main: './main.js',
        defaultExtension: 'js'
      }
    },
    meta: {
      '*.js': {
        babelOptions: {
          stage1: true,
          stage2: true,
          es2015: true
        }
      },
      '*.css': { loader: 'css' }
    }
  })
}(this))
