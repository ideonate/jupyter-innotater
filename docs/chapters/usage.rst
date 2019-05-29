Usage Reference
---------------

Innotater
~~~~~~~~~

::

    Innotater( inputs, targets, indexes=None, keyboard_shortcuts=True )

Instantiates the Jupyter widget. Each of ``inputs`` and ``targets`` is
an Innotation subclass or array of Innotation subclasses.

The Innotation subclasses allow display and interaction with different
types of input/target data. Typically, inputs contains one or more data
source that is fixed in your project (e.g. images of dogs) and targets
contains data that is intended to be modified through the widget.

To display the widget explicitly:

::

    w = Innotater( inputs, targets )
    display(w)

``indexes`` is an optional array containing either integers or booleans
instructing the widget to display only a subset of the inputs and
targets, allowing you to focus on interesting items only. If ``indexes``
is an integer array it must contain index values. For example, if
inputs/targets has 10 data samples, then indexes=[0,3,5] would cause the
widget to show only 3 possible data samples - the 1st, 4th, and 6th of
the original data source. If ``indexes`` is a boolean mask array it must
have the same length as the original data source, and the widget will
only show those data samples corresponding to True in the indexes array.
The flag ``keyboard_shortcuts`` can be set to False to disable keyboard
shortcuts - namely 'n' and 'p' for next/previous.

Innotation subclasses
~~~~~~~~~~~~~~~~~~~~~

This is the base class (not to be instantiated directly).

The general constructor format for subclasses is:

::

    Innotation( <array_like> data, [name=<string>,] [desc=<string>,] [layout=<dict>,])

Optionally, data can be specified as a ``data=`` keyword argument, in
which case the positional data argument should be omitted.

``name`` is optional unless required so that the Innotation can be
specified as the source for another Innotation (e.g. to link the
Bounding Box data with the image to which it applies).

``desc`` is also optional, and defaults to the same value as ``name``.
It may be displayed as a text label next to the data in the widget.

``layout`` is an optional dictionary of CSS styles to pass on to the
underlying widget, for example layout={'width':'100px'}

ImageInnotation
^^^^^^^^^^^^^^^

data is expected to be an array of filenames, blobs, or numpy arrays
containing image data directly (RGB format).

Extra optional parameters:

``path`` - a path to be prefixed to all filenames provided in data.

``width`` and/or ``height`` to specify the maximum size of image to
display as an integer number of pixels. For example, if you specify only
width=300 then images will be scaled down to a width of 300 pixels if
the image is larger, or will display at their original size if their
width is <300 pixels. Similarly, ``height`` can be specified alone, or
``width`` and ``height`` specified together to fix the shape of the
image display precisely, with the image scaled proportionally to fit if
required. Any bounding box co-ordinates recorded will always be relative
to the original image dimensions.

``transform`` is any function to be applied to each image entry in data
before it is processed to be displayed on the screen. For example, you
might set ``transform`` to a denormalization function because all images
in data have been normalized for training purposes.

BoundingBoxInnotation
^^^^^^^^^^^^^^^^^^^^^

data is expected to be a 2-dimensional array with four columns
corresponding to x,y,w,h - the top-left co-ordinates of the bounding
boxes and width/height.

Displays a text box containing x,y,w,h as a string which can be edited
directly or by drawing a bounding box on the corresponding
ImageInnotation.

If there is only one ImageInnotation in the Innotater instance, that
will be assumed to be the source image for this BoundingBoxInnotation.
If there are multiple images, the source parameter will be needed (see
below).

Extra parameters:

``source`` - the ``name`` attribute of the corresponding ImageInnotation
(required if there is ambiguity). Example:

::

    Innotater( [ ImageInnotation(foodimages, name='food'), ImageInnotation(maskimages, name='mask'),], BoundingBoxInnotation(targets, source='food') )

In this example, the first image (with ``name='food'``) will allow the
user to draw a bounding box on it, and this will update the co-ordinates
in the BoundingBoxInnotation (which has ``source='food'``)

MultiClassInnotation
^^^^^^^^^^^^^^^^^^^^

data is expected to be one of:

-  simple 1-dim array\_like of integers representing the class index
-  2-dim column vector (second dim has size 1) still containing only
   integers representing the class index
-  2-dim one-hot encoding

Displays a list selection box so the user can choose one highlighted
option. Currently does not support multiple selections per row.

Extra optional parameters:

``classes`` - an array of string values containing text to display in
place of the numerical class indices. Will try to infer from data if
omitted.

``dropdown`` - boolean to indicate if the widget should be shown as a
Dropdown list (True) or the default value of a larger always-open list
(False)

BinaryClassInnotation
^^^^^^^^^^^^^^^^^^^^^

data is expected to be an array of True/False values.

Displays a checkbox.

Extra optional parameters:

``classes`` - an array of two string values containing text to display
in place of 'False' and 'True'.

TextInnotation
^^^^^^^^^^^^^^

data is expected to be an array of text strings.

Displays a textarea showing the text.
