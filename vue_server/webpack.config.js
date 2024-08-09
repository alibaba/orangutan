const MonacoEditorPlugin = require('monaco-editor-webpack-plugin')
module.exports = {
  plugins: [
    new MonacoEditorPlugin({
      languages: ['python']
    })
  ]
}