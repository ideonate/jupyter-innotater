var widgets = require('@jupyter-widgets/base');

var controls = require('@jupyter-widgets/controls');

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


var InnotaterImagePadModel = controls.ImageModel.extend({
	defaults: _.extend(controls.ImageModel.prototype.defaults(), {
		_model_name: 'InnotaterImagePadModel',
		_view_name: 'InnotaterImagePadView',
		_model_module: 'jupyter-innotater',
		_view_module: 'jupyter-innotater',
		_model_module_version: '0.1.0',
		_view_module_version: '0.1.0'
	})
});


// Custom View. Renders the widget model.
var InnotaterImagePadView = widgets.DOMWidgetView.extend({

	InnotaterImagePadView: function() {
		this.imageLoaded = false;
		InnotaterImagePadView.__super__.apply(this, arguments);
	},

	render: function () {
		/**
		 * Called when view is rendered.
		 */
		//_super.prototype.render.call(this);
		InnotaterImagePadView.__super__.render.apply(this, arguments);
		this.pWidget.addClass('jupyter-widgets');
		this.pWidget.addClass('widget-image');

		this.imgel = new Image(); //$('<img></img>')[0];

		this.canvas = $('<canvas></canvas>')[0];

		this.$el.append($('<div></div>').append(this.canvas));

		var self = this;

		self.rectX = 0;
		self.rectY = 0;
		self.rectW = 0;
		self.rectH = 0;

		var $canvas = $(self.canvas);
		$(this.canvas).on('mousedown', function(e) {
			var p = $canvas.offset();
			self.rectX = e.pageX - p.left;
			self.rectY = e.pageY - p.top;
		}).on('mousemove', function(e) {
	
		}).on('mouseup', function(e) {
			var p = $canvas.offset();
			self.rectW = e.pageX - p.left - self.rectX;
			self.rectH = e.pageY - p.top - self.rectY;
			self.update();
		});

		this.update();
	},

	update: function () {
		/**
		 * Update the contents of this view
		 *
		 * Called when the model is changed.  The model may have been
		 * changed by another view or by a state update from the back-end.
		 */
		this.imageLoaded = false;

		var url;
		var format = this.model.get('format');
		var value = this.model.get('value');
		if (format !== 'url') {
			var blob = new Blob([value], { type: "image/" + this.model.get('format') });
			url = URL.createObjectURL(blob);
		}
		else {
			url = (new TextDecoder('utf-8')).decode(value.buffer);
		}
		// Clean up the old objectURL
		var oldurl = this.imgel.src;
		this.imgel.src = url;
		if (oldurl && typeof oldurl !== 'string') {
			URL.revokeObjectURL(oldurl);
		}
		var width = this.model.get('width');
		if (width !== undefined && width.length > 0) {
			this.imgel.setAttribute('width', width);
		}
		else {
			this.imgel.removeAttribute('width');
		}
		var height = this.model.get('height');
		if (height !== undefined && height.length > 0) {
			this.imgel.setAttribute('height', height);
		}
		else {
			this.imgel.removeAttribute('height');
		}


		var self = this;
		this.imgel.onload = function() {
			self.canvas.setAttribute('width', self.imgel.width);
			self.canvas.setAttribute('height', self.imgel.height);

			this.imageLoaded = true;

			self.drawCanvas();
		}

		//return _super.prototype.update.call(this);
		return InnotaterImagePadView.__super__.update.apply(this, arguments);
	},

	drawCanvas: function() {
		var ctx = this.canvas.getContext('2d');
		ctx.drawImage(this.imgel, 0, 0);
		ctx.rect(this.rectX, this.rectY, this.rectW, this.rectH);
		ctx.stroke();
	},

	remove: function() {
		if (this.imgel.src) {
			URL.revokeObjectURL(this.imgel.src);
		}
		//_super.prototype.remove.call(this);
		InnotaterImagePadView.__super__.remove.apply(this, arguments);
	}
});

Object.defineProperty(InnotaterImagePadView.prototype, "tagName", {
	/**
	 * The default tag name.
	 *
	 * #### Notes
	 * This is a read-only attribute.
	 */
	get: function () {
		// We can't make this an attribute with a default value
		// since it would be set after it is needed in the
		// constructor.
		return 'div';
	},
	enumerable: true,
	configurable: true
});

module.exports = {
    InnotaterImagePadModel: InnotaterImagePadModel,
    InnotaterImagePadView: InnotaterImagePadView
};



