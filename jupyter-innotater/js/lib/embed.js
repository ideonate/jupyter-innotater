// Entry point for the unpkg bundle containing custom model definitions.
//
// It differs from the notebook bundle in that it does not need to define a
// dynamic baseURL for the static assets and may load some css that would
// already be loaded by the notebook otherwise.

// This file is currently being required by index.js entry point too

// Export widget models and views, and the npm package version number.
var _ = require('lodash');

module.exports = require('./innotaterwidget.js');
_.extend( module.exports, require('./imagewidget.js') );
_.extend( module.exports, require('./customwidgets.js') );
module.exports['version'] = require('../package.json').version;