// Export widget models and views.
var _ = require('lodash');

var innotater = require('./innotaterwidget.js');
_.extend( innotater, require('./imagewidget.js') );
_.extend( innotater, require('./customwidgets.js') );


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
