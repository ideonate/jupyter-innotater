
var innotater = require('./embed.js');

var base = require('@jupyter-widgets/base');

module.exports = [{
    id: 'jupyter-innotater',
    requires: [base.IJupyterWidgetRegistry],
    autoStart: true,
    activate: function(app, widgets) {

        widgets.registerWidget({
            name: 'jupyter-innotater',
            version: innotater.version,
            exports: innotater
        });

    }
}];
