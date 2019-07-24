"use strict";
//Object.defineProperty(exports, "__esModule", { value: true });

var innotater = require('./embed.js');

var base = require('@jupyter-widgets/base');

const innotaterPlugin = {
    id: 'jupyter-innotater',
    requires: [base.IJupyterWidgetRegistry],
    activate: function(app, widgets) {
        console.log("JL Innotater activated");
        console.log(innotater.version);

        widgets.registerWidget({
            name: 'jupyter-innotater',
            version: innotater.version,
            exports: innotater
        });
    },
    autoStart: true
};

exports.default = innotaterPlugin;
