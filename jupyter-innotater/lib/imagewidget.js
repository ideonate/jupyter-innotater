var widgets = require('@jupyter-widgets/base');
var controls = require('@jupyter-widgets/controls');

require("../style/index.css");

var _ = require('lodash');

var $ = require('jquery');


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

var version = require('../package.json').version;

var InnotaterImagePadModel = controls.ImageModel.extend({
	defaults: _.extend(controls.ImageModel.prototype.defaults(), {
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
		var self = this;

		InnotaterImagePadView.__super__.render.apply(this, arguments);
		this.pWidget.addClass('jupyter-widgets');
		this.pWidget.addClass('widget-image');

		this.imgel = new Image();

		this.canvas = $('<canvas></canvas>', {'class': 'jupyter-innotater-imagepad'})[0];

		this.$el.append($('<div></div>').append(this.canvas));

		self.rectX = 0;
		self.rectY = 0;
		self.rectW = 0;
		self.rectH = 0;
		self.isSelecting = false;

		var $canvas = $(self.canvas);
		$(this.canvas).on('mousedown', function(e) {
			if (self.is_bb_source && e.which == 1) {
				self.p = $canvas.offset();
				self.rectX = (e.pageX - self.p.left) / self.zoom;
				self.rectY = (e.pageY - self.p.top) / self.zoom;
				self.isSelecting = true;
				self.rectW = 0;
				self.rectH = 0;
			}
		}).on('mousemove', function(e) {
			if (self.isSelecting) {
				self.rectW = (e.pageX - self.p.left) / self.zoom  - self.rectX;
				self.rectH = (e.pageY - self.p.top) / self.zoom - self.rectY;
				self.drawCanvas();
			}
		}).on('mouseup mouseleave', function(e) {
			if (self.isSelecting) {
				self.rectW = Math.round((e.pageX - self.p.left) / self.zoom  - self.rectX);
				self.rectH = Math.round((e.pageY - self.p.top) / self.zoom - self.rectY);

				self.rectX = Math.round(self.rectX); // Wait until rectW/H calculated to avoid rounding the difference twice
				self.rectY = Math.round(self.rectY);

				// Check bounds and adjust
				if (self.rectW < 0) {
					self.rectX += self.rectW;
					self.rectW = -self.rectW;
				}
				if (self.rectH < 0) {
					self.rectY += self.rectH;
					self.rectH = -self.rectH;
				}

				if (self.rectX < 0) { self.rectX = 0; }
				if (self.rectY < 0) { self.rectY = 0; }
				if (self.rectX + self.rectW > self.imgel.width) { self.rectW = self.imgel.width - self.rectX; }
				if (self.rectY + self.rectH > self.imgel.height) { self.rectH = self.imgel.height - self.rectY; }

				// Sync to backend
				var rects = _.clone(self.model.get('rects'));
				var rect_index = self.model.get('rect_index');
				var max_repeats = self.model.get('max_repeats');
				while (rects.length < (rect_index+1)*4) {
					rects.push(0);
				}

				rects[rect_index*4] = self.rectX;
				rects[rect_index*4+1] = self.rectY;
				rects[rect_index*4+2] = self.rectW;
				rects[rect_index*4+3] = self.rectH;
				rect_index = (rect_index + 1) % max_repeats;
				self.model.set({'rects': rects,  'rect_index': rect_index});
				// self.model.set({'rect': [self.rectX, self.rectY, self.rectW, self.rectH]});
				self.model.save_changes();
				self.isSelecting = false;

				//self.update will be called automatically because model was changed
			}
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

		var new_is_bb_source = this.model.get('is_bb_source');

		if (new_is_bb_source != this.is_bb_source) {
			if (new_is_bb_source) {
				$(this.canvas).addClass('is_bb_source');
			}
			else {
				$(this.canvas).removeClass('is_bb_source');
			}
			this.is_bb_source = new_is_bb_source;
		}

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


		// Get bounding box from model

		/*var rect_index = this.model.get('rect_index');
		var r = _.clone(this.model.get('rects'));

		while (r.length < (rect_index+1)*4) {
			r.push(0);
		}

		this.rectX = r[rect_index*4];
		this.rectY = r[rect_index*4+1];
		this.rectW = r[rect_index*4+2];
		this.rectH = r[rect_index*4+3]; */

		this.usewidth = 0;
		this.useheight = 0;
		this.zoom = 1.0;

		var self = this;
		this.imgel.onload = function() {


			var wantwidth = self.model.get('wantwidth');
			var wantheight = self.model.get('wantheight');

			self.usewidth = 0;
			self.useheight = 0;

			if (wantwidth !== undefined && wantwidth > 0) {
				self.usewidth = wantwidth;
				self.canvas.setAttribute('width', wantwidth.toString());

				if (wantwidth > self.imgel.width) {
					self.usewidth = self.imgel.width;
					self.zoom = 1.0;
				}
				else {
					self.usewidth = wantwidth;
					self.zoom = wantwidth / self.imgel.width;
				}
			}
			else {
				self.usewidth = self.imgel.width;
				self.zoom = 1.0;
				self.canvas.setAttribute('width', self.imgel.width.toString());
			}

			self.useheight = self.imgel.height * self.zoom;
			if (wantheight !== undefined && wantheight > 0) {
				// Take wantheight as a max height, zoom further if needed
				self.canvas.setAttribute('height', wantheight.toString());

				if (self.useheight > wantheight) {
					self.useheight = wantheight;
					self.zoom = wantheight / self.imgel.height;
					self.usewidth = self.imgel.width * self.zoom;
					if (wantwidth == undefined || wantwidth <= 0) {
						// wantwidth wasn't specified, so cut width further
						self.canvas.setAttribute('width', self.usewidth.toString());
					}
				}
			}
			else {
				self.canvas.setAttribute('height', self.useheight.toString());
			}

			self.imageLoaded = true;

			self.drawCanvas();
		}

		return InnotaterImagePadView.__super__.update.apply(this, arguments);
	},

	drawCanvas: function() {
		var self = this;
		var ctx = this.canvas.getContext('2d');

		ctx.fillStyle = 'lightGrey';
		ctx.fillRect(0,0,self.canvas.width,self.canvas.height);

		ctx.drawImage(this.imgel, 0, 0, self.usewidth, self.useheight);

		if (self.is_bb_source) {
			var rect_index = this.model.get('rect_index');
			var r = _.clone(this.model.get('rects'));
			var max_repeats = this.model.get('max_repeats');

			var ann_styles = this.getAnnotationStyles();

			for (var ri=0; ri < max_repeats; ri++) {
				if (ri != rect_index || !self.isSelecting) {
					self.drawBox(ctx, r[ri * 4], r[ri * 4 + 1], r[ri * 4 + 2], r[ri * 4 + 3], ann_styles, ri == rect_index);
				}
			}

			if (self.isSelecting) {
				self.drawBox(ctx, self.rectX, self.rectY, self.rectW, self.rectH, ann_styles, true);
			}
		}
	},

	drawBox: function(ctx, x,y,w,h, ann_styles, isdrawing) {

		ctx.save();
		ctx.globalAlpha = 0.9;

		ctx.beginPath();
		ctx.strokeStyle = ann_styles[isdrawing ? 'selected_color1' : 'color1'];
		ctx.lineWidth = ann_styles['lineWidth'];
		ctx.rect(x*this.zoom, y*this.zoom, w*this.zoom, h*this.zoom);
		ctx.stroke();

		ctx.beginPath();
		ctx.strokeStyle = ann_styles[isdrawing ? 'selected_color2' : 'color2'];
		ctx.lineWidth = ann_styles['lineWidth'];
		var ld = ann_styles['lineDash'];
		if (typeof ld == 'number') {
			ld = [ld];
		}
		ctx.setLineDash(ld);
		ctx.rect(x*this.zoom, y*this.zoom, w*this.zoom, h*this.zoom);
		ctx.stroke();

		ctx.restore();
	},

	getAnnotationStyles : function() {
		return _.defaults(this.model.get('annotation_styles'), {
			'color1': '#FFFFFF',
			'color2': '#000000',
			'lineDash': [2],
			'lineWidth': 1,
			'selected_color1': '#FFFFFF',
			'selected_color2': '#008000',
		});
	},

	remove: function() {
		if (this.imgel.src) {
			URL.revokeObjectURL(this.imgel.src);
		}
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



