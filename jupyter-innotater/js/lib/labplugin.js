var innotater = require('./embed.js');

var base = require('@jupyter-widgets/base');

module.exports = {
    id: 'innotater',
    requires: [base.IJupyterWidgetRegistry],
    activate: function(app, widgets) {
        widgets.registerWidget({
            name: 'innotater',
            version: innotater.version,
            exports: innotater
        });
    },
    autoStart: true
};

