var widgets = require('@jupyter-widgets/base');
var controls = require('@jupyter-widgets/controls');

require("./style.css");

var _ = require('lodash');

var $ = require('jquery');


var FocusTextView = widgets.TextView.extend({

    events: function () {
        console.log("EVENTS !!!");
        var d = FocusTextView.__super__.events(this, arguments);
        d['click input'] = 'handleFocus';
        return d;
    }

});

FocusTextView.prototype.handleFocus = function(e) {
    this.send({ event: 'click' });
};

module.exports = {
    FocusTextView: FocusTextView
};

