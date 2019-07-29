var path = require('path');
var version = require('./package.json').version;
var WebpackBuildNotifierPlugin = require('webpack-build-notifier');

// Custom webpack rules are generally the same for all webpack bundles, hence
// stored in a separate local variable.
var rules = [
	{ test: /\.css$/, use: ['style-loader', 'css-loader'] },
	{ test: /\.less$/, use: ['style-loader', 'css-loader', 'less-loader'] },
	{
		test: /\.(js|ts)$/,
		use: ['source-map-loader'],
		enforce: 'pre'
	}
];

var resolve = {
	extensions: ['.js']
};

module.exports = [
	{// Notebook extension
		//
		// This bundle only contains the part of the JavaScript that is run on
		// load of the notebook. This section generally only performs
		// some configuration for requirejs, and provides the legacy
		// "load_ipython_extension" function which is required for any notebook
		// extension.
		//
		entry: './lib/extension.js',
		resolve: resolve,
		output: {
			filename: 'extension.js',
			path: path.resolve(__dirname, '..', 'jupyter_innotater', 'static'),
			libraryTarget: 'amd'
		},
		devtool: 'source-map'
	},
	{// Bundle for the notebook containing the custom widget views and models
		//
		// This bundle contains the implementation for the custom widget views and
		// custom widget.
		// It must be an amd module
		//
		entry: './lib/index.js',
		resolve: resolve,
		output: {
			filename: 'index.js',
			path: path.resolve(__dirname, '..', 'jupyter_innotater', 'static'),
			libraryTarget: 'amd'
		},
		devtool: 'source-map',
		module: {
			rules: rules
		},
		externals: ['@jupyter-widgets/base', '@jupyter-widgets/controls'],
		plugins: [
			new WebpackBuildNotifierPlugin({
				title: "Webpack notebook build of Innotater",
				sound: 'Basso',
				successSound: 'Ping'
			})
		]
	},
	{// Embeddable widget-innotater bundle
		//
		// This bundle is generally almost identical to the notebook bundle
		// containing the custom widget views and models.
		//
		// The only difference is in the configuration of the webpack public path
		// for the static assets.
		//
		// It will be automatically distributed by unpkg to work with the static
		// widget embedder.
		//
		// The target bundle is always `dist/index.js`, which is the path required
		// by the custom widget embedder.
		//
		entry: './lib/embed.js',
		resolve: resolve,
		output: {
			filename: 'index.js',
			path: path.resolve(__dirname, 'dist'),
			libraryTarget: 'amd',
			publicPath: 'https://unpkg.com/jupyter-innotater@' + version + '/dist/'
		},
		devtool: 'source-map',
		module: {
			rules: rules
		},
		externals: ['@jupyter-widgets/base', '@jupyter-widgets/controls']
	}
];
