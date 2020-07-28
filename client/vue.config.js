// const IS_PRODUCTION = process.env.NODE_ENV === 'production'
const path = require('path')

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  // publicPath : 'public',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  lintOnSave: process.env.NODE_ENV !== 'production',
  devServer: {
    // public: '192.168.86.100',
    // port: '8080',
    overlay: {
      warnings: true,
      errors: false
    },
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to flask` dev server
        target: 'http://localhost:5000/'
      }
    }
  }
}
