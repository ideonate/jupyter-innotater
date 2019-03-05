# jupyter-innotater

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/PierreMarion23/jupyter-widget-drawing-pad-binder/master)

## 1 - Overview

This is a simple widget inspired by a drawing pad (see [this example](https://codepen.io/anon/pen/aLYeNB)). Thanks to this widget, you can draw in a box whatever you want (for instance a signature). The coordinates of the points of the trajectory is synchronised with the Python kernel.

You'll find some additional functionalities :
+ a `Save` button with a text field in order to save your signature along with your name
+ a `Clear` button to clear what is drawn in the box
+ a `Login` button : by entering your name (after having saved a signature for this name) and drawing your signature, a message `Welcome (name)` should appear (if the signature is close enough to the saved one)

When you try to login, the comparison between the signature to the registered one takes into account not only the spatial coordinates but also time.

To get a feel of the result check out the [demo notebook](https://github.com/ocoudray/jupyter-drawing-pad/blob/master/Example/Demo_drawing_pad.ipynb).


The official documentation describes a [Hello World](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Custom.html) widget and also points to several very [advanced widgets](http://jupyter.org/widgets.html) from [bqplot](https://github.com/bloomberg/bqplot) to [ipyvolume](https://github.com/maartenbreddels/ipyvolume).  
But there is a large gap between these 2 stages.  

This simple widget may serve as a template for intermediate users who feel the (huge) potential of this library, want to build one, but cannot find examples relevant to their level i.e. past absolute beginner.

For more info about jupyter widgets (installation process, packaging and publishing), see [this tutorial repo](https://github.com/ocoudray/first-widget). All what's written there is also true for this package, just changing the name `first-widget` into `jupyter-drawing-pad`.


## 2 - Installation

    $ pip install jupyter_drawing_pad
