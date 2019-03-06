var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var $ = require('jquery');
//var drawing_pad = require('./drawing-pad');


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.


var InnotaterModel = widgets.DOMWidgetModel.extend({
	defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
		_model_name: 'InnotaterModel',
		_view_name: 'InnotaterView',
		_model_module: 'jupyter-innotater',
		_view_module: 'jupyter-innotater',
		_model_module_version: '0.1.0',
		_view_module_version: '0.1.0',

		inputs : [],
		targets : [],
		path: '',
		index: 0

	})
});


// Custom View. Renders the widget model.
var InnotaterView = widgets.DOMWidgetView.extend({
	render: function () {
		InnotaterView.__super__.render.apply(this, arguments);
		//this._index_changed();
		//this.listenTo(this.model, 'change:index', this._index_changed, this);
		//this.listenTo(this.model, 'change:checkbox_value', this._checkbox_value_changed, this);
		//this.listenTo(this.model, 'change:inputs', this._index_changed, this);
		//this.listenTo(this.model, 'change:targets', this._index_changed, this);
	},

	_index_changed: function () {
		/*var old_value = this.model.previous('index');
		var index = this.model.get('index');
		var path = this.model.get('path');
		var inputs = this.model.get('inputs');
		var targets = this.model.get('targets').slice();

		var domcontainer = $('<div></div>');
		var domimage = $('<img></img>', {'src': path+inputs[index], 'width': '150', 'height': '100'});
		var domtext = $('<div></div>').append(String(index));

		var cur_value = targets[index];

		this.model.set('checkbox_value', !!cur_value);
		this.model.save_changes();

		domcontainer.append(domimage).append(domtext);

		$(this.el).empty().append(domcontainer); */
	},

	_checkbox_value_changed: function() {
		var index = this.model.get('index');
		var targets = this.model.get('targets').slice();

		var cur_value = !!targets[index];
		var new_value = this.model.get('checkbox_value');

		if (new_value != cur_value) {
			targets[index] = Number(new_value); // Need 0/1 not false/true
			console.log(targets);
			this.model.set({'targets': targets});
			console.log(this.model.get('targets'));
			this.model.save_changes();
			console.log(this.model.get('targets'));
		}
	}
});


module.exports = {
	InnotaterModel: InnotaterModel,
	InnotaterView: InnotaterView
};

