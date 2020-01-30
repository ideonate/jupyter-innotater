Usage Reference
---------------

Innotater
~~~~~~~~~

::

    Innotater( inputs, targets, indexes=None, keyboard_shortcuts=True, save_hook=None )

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
shortcuts - namely 'n' and 'p' for next/previous, and 's' for save if a
save_hook is supplied.

``save_hook`` is an optional Python function. If
supplied, a Save button will appear in the Innotater, and your function
will be called when it is clicked.
Your function should be of the form ``my_save_hook(uindexes)`` where
``uindexes`` is a list of indexes of data samples that have changed and
need to be saved to permanent storage. The function should return True
if the data is saved successfully.
See Example/Hooks.ipynb for an example save hook.

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
(or similar, e.g. PyTorch Tensor) containing image data directly.

Extra optional parameters:

``path`` - a path to be prefixed to all filenames provided in ``data``
(this parameter is ignored if ``data`` does not contain filenames).

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

``colorspace`` is a string containing either 'RGB' or 'BGR' (default is
'BGR'). This only has an effect if you pass numpy arrays or similar as
the ``data`` attribute. It specifies the meaning of the color channels
of the input data. For example, if you load images using Open CV2
(cv2.imread) then the default of 'BGR' will normally be correct; if you
load images via matplotlib imread, you will likely need colorspace to be
'RGB'.

Note that if a numpy array is provided channel-first, the Innotater
should detect this and automatically switch the channel to be the last
axis internally.

``annotation_styles`` is an optional dict to control how bounding
boxes are displayed to the user. Defaults will be used for any keys
omitted. For example:

::

  ImageInnotation( images, annotation_styles = {
        'color1': '#FF0000', /* strokeStyle in Javascript context */
        'color2': '#00FF00', /* For second color of the dashed line */
        'lineWidth': 5, /* lineWidth in JS context */
        'lineDash': [10, 1, 5], /* Passed to setLineDash, can take one int instead of array */
        'selected_color2': '#FFFFFF', /* color1 but for currently-selected box */
        'selected_color2': '#0000AA', /* color2 for currently-selected box */
  } )


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

ButtonInnotation
^^^^^^^^^^^^^^^^

This displays a button where you can supply custom functionality.

data must be supplied but can be None since it is ignored.

The button will be given the label supplied in the ``desc`` field.

``on_click`` parameter is a Python function that will be called when the button is clicked. It should be of
the form ``my_click_handler(uindex, repeat_index, **kwargs)`` where ``uindex`` is the underlying index of the
data sample where the button was clicked, and ``repeat_index`` is the row within a ``RepeatInnotation`` (see below) or
-1 if not within any repeat row. ``kwargs`` will contain ``desc`` and ``name`` values.
Your function should return True if the data sample at ``uindex`` has been changed so needs be updated in the
Innotater's display; False otherwise,

See the example notebook in Example/Hooks.ipynb for typical usage of ``ButtonInnotation``.

Repeats and Grouping
~~~~~~~~~~~~~~~~~~~~

There are two special Innotations that control grouping or repeating of multiple other ordinary Innotations.

RepeatInnotation
^^^^^^^^^^^^^^^^

Specify an arbitrary number of repeats of a series of Innotation types. The constructor is:

::

    RepeatInnotation( *configuration_tuples, [min_repeats=0,] [max_repeats=10] )

Where ``configuration_tuples`` is an array of one or more tuples of length 2 or 3 and of the following form:

::

    ( InnotationSubclass, data [, construction_kwargs] )

Where:

 * ``InnotationSubclass`` is a subclass of ``Innotation`` (e.g. BoundingBoxInnotation), NOT an instance of the subclass.
 * ``data`` is a matrix that can be used by ``InnotationSubclass`` to store the data as normal, except this should have an
   extra dimension (typically of size ``max_repeats``) inserted as the second dimension compared to the same Innotation
   subclass if used directly without RepeatInnotation.
 * ``construction_kwargs`` is an optional dict that will be passed as \*\*kwargs when each InnotationSubclass is
   instantiated by the RepeatInnotation.

So for each row of Innotations to be added, for each tuple in ``configuration_tuples``, each subclass will be
instantiated by RepeatInnotation itself as follows:

::

    InnotationSubclass( data, \*\*construction_kwargs )

The :ref:`multiple` are the best way to understand how this works!

GroupedInnotation
^^^^^^^^^^^^^^^^^

Group two or more Innotations together horizontally so they appear side-by-side instead of vertically.

::

    GroupedInnotation( *innotation_list )

Where ``innotation_list`` is just an '\*args' list of ordinary Innotation objects, e.g. a BoundingBoxInnotation and a
MultiClassInnotation so that the bounding box textbox appears side-by-side with a dropdown.


