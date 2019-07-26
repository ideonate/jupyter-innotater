
var innotater = require('./embed.js');

//     "@jupyter-widgets/controls": "^1.5.0",

//     "@jupyter-widgets/base": "^2.0",

var base = require('@jupyter-widgets/base');

module.exports = [{
    id: 'jupyter-innotater',
    requires: [base.IJupyterWidgetRegistry],
    autoStart: true,
    activate: function(app, widgets) {
        console.log("JL Innotater activated");

        widgets.registerWidget({
            name: 'jupyterinnotater',
            version: innotater.version,
            exports: innotater
        });

    }
}];

console.log("JL Innotater loaded");
