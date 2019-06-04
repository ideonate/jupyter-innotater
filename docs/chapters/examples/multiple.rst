.. _multiple:


Multiple Examples
~~~~~~~~~~~~~~~~~

Examples using RepeatInnotation to specify arbitrary numbers of multiple sub-Innotations (e.g. multiple bounding boxes
with corresponding dropdowns to classify each box).

See `Example/Examples-multiple.ipynb <https://github.com/ideonate/jupyter-innotater/blob/master/Example/Examples-multiple.ipynb>`__
to run similar examples interactively. Try running
`Examples-multiple.ipynb on
Binder <https://mybinder.org/v2/gh/ideonate/jupyter-innotater/master?filepath=Example%2FExamples-multiple.ipynb>`__
for free with no setup required!


Multiple Bounding Boxes (with single multi-classification)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

For each photo, select whether it depicts 'cats' or 'dogs', and then draw multiple bounding boxes to depect each of the
animals present in the photo. This assumes that each photo will either contain all cats or all dogs.

Notice that the BoundingBoxInnotation is not instantiated directly in our code - the RepeatInnotation takes care of
that depending on how many Bounding Boxes we actually need.

Note also that compared to the :ref:`single` examples, the `targets_bboxes` matrix has an extra dimension.

::

    from jupyter_innotater import *

    animalfns = sorted(os.listdir('./animals/'))

    repeats = 8

    # Per-photo data
    classes = ['cat', 'dog']
    targets_type = np.zeros((len(animalfns), len(classes)), dtype='int') # One-hot encoding

    # Repeats within each photo
    targets_bboxes = np.zeros((len(animalfns), repeats, 4), dtype='int') # (x,y,w,h) for each animal

    Innotater(
        ImageInnotation(animalfns, path='./animals', width=400, height=300),
        [
            MultiClassInnotation(targets_type, name='Animal Type', classes=classes, dropdown=False),
            RepeatInnotation(
                (BoundingBoxInnotation, targets_bboxes),
                 max_repeats=repeats, min_repeats=1
            )
        ]
    )

.. figure:: ../../_static/screenshots/MultipleBBoxesSingleClass.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter

The 'Add' button allows you to insert extra bounding boxes if needed, up to a maximum of 8 in this case. Once
added the extra boxes appear, they will all be present on every photo as you step through.

::

    print('One-hot classes', targets_type[:2]) # Just display the first 2 to save space
    print('Bounding Boxes', targets_bboxes[:2])

Output:

::

    One-hot classes [[1 0]
     [0 1]]

    Bounding Boxes [[[ 79   5 143 242]
      [182  15  84  95]
      [225  83  97 163]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]]

     [[  8  54 171 246]
      [204   8 196 282]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]
      [  0   0   0   0]]]


Multiple Bounding Boxes AND Multi-classification
++++++++++++++++++++++++++++++++++++++++++++++++

For each photo, draw multiple bounding boxes and specify for each bounding box what is depicted (from a dropdown).

There is also an 'Exclude' checkbox per photo so we can select if that photo should be excluded from the dataset - you
would write some code to remove those before full processing later on.

Also display the filename in a textbox, for information only.

::

    from jupyter_innotater import *

    animalfns = sorted(os.listdir('./animals/'))

    repeats = 4

    # Per-photo data
    targets_exclude = np.zeros((len(animalfns), 1), dtype='int') # Binary flag to indicate want to exclude from dataset

    # Repeats within each photo
    breeds = ['Cat - Shorthair tabby', 'Cat - Shorthair ginger', 'Dog - Labrador', 'Dog - Beagle', 'Dog - Terrier']
    targets_breed = np.zeros((len(animalfns), len(classes)), dtype='int')
    targets_bboxes = np.zeros((len(animalfns), repeats, 4), dtype='int') # (x,y,w,h) for each animal

    Innotater(
        [
            ImageInnotation(animalfns, path='./animals', width=370, height=280), # Display the image itself
            TextInnotation(animalfns, multiline=False) # Display the image filename
        ],
        [
            BinaryClassInnotation(targets_exclude, name='Exclude'), # Checkbox
            RepeatInnotation(
                (BoundingBoxInnotation, targets_bboxes), # Individual animal bounding box
                (MultiClassInnotation, targets_breed,
                    {'name':'Breed', 'classes':breeds, 'dropdown':True}), # Per-animal breed dropdown
                max_repeats=repeats, min_repeats=1
            )
        ]
    )

.. figure:: ../../_static/screenshots/MultipleBBoxesANDMultiClass.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter

::

    print('One-hot Exclude', targets_exclude[:2]) # Just display the first 2 to save space
    print('Animal Bounding Boxes', targets_bboxes[:2])
    print('Animal Breeds', targets_breed[:2])

Output:

::

    One-hot Exclude [[0]
     [0]]

    Animal Bounding Boxes [[[ 77  10 136 235]
      [186  11  86  99]
      [230  80  97 169]
      [  0   0   0   0]]

     [[  0  55 175 245]
      [213   2 187 295]
      [  0   0   0   0]
      [  0   0   0   0]]]

    Animal Breeds [[[0 0 0 0 0]
      [0 0 0 0 0]
      [0 0 0 0 0]
      [0 0 0 0 0]]

     [[0 0 0 1 0]
      [0 0 0 0 1]
      [0 0 0 0 0]
      [0 0 0 0 0]]]


Grouping
++++++++

It is possible to use GroupedInnotation to wrap other Innotation objects. This simply means they will be displayed
side-by-side.

For example:

::

    targets_singlebb = np.zeros((len(animalfns), 4), dtype='int') # (x,y,w,h) for each data row
    targets_cl = np.zeros((len(animalfns), 1), dtype='int')

    Innotater(
        ImageInnotation(animalfns, path='./animals', width=370, height=280),
        GroupedInnotation( # Just to place side-by-side
            MultiClassInnotation(targets_cl, name='Animal', classes=classes, dropdown=True),
            BoundingBoxInnotation(targets_singlebb)
        )
    )


This will be functionally similar to the same code but using a list to wrap the MultiClassInnotation and
BoundingBoxInnotation instead of the GroupedInnotation, but the Bounding Box textbox and Dropdown will appear next to
each other instead of one above the other.

In contrast to RepeatInnotation, this *does* accept ready-instantiated Innotations rather than the class names as
configuration.
