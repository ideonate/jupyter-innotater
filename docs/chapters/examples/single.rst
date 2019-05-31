.. _single:


Single Examples
~~~~~~~~~~~~~~~

See `Example/Examples.ipynb <https://github.com/ideonate/jupyter-innotater/blob/master/Example/Examples.ipynb>`__
to run similar examples interactively. Try running
`Examples.ipynb on
Binder <https://mybinder.org/v2/gh/ideonate/jupyter-innotater/master?filepath=Example%2FExamples.ipynb>`__
for free with no setup required!

Images and Bounding Boxes
+++++++++++++++++++++++++

Load some images from filenames in an array, initialise empty bounding
boxes.

Then set up Innotater to display the images so you can draw updated
bounding boxes directly.

::

    from jupyter_innotater import *

    import numpy as np, os

    images = os.listdir('./foods/')
    targets = np.zeros((len(images), 4)) # Initialise bounding boxes as x,y = 0,0, width,height = 0,0

    Innotater( ImageInnotation(images, path='./foods'), BoundingBoxInnotation(targets) )

.. figure:: ../../_static/screenshots/ImageAndBBoxesInnotater.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter

The widget allows you to interactively draw bounding boxes for any of
the images, and the ``targets`` variable is always kept in sync with
your changes.

Advance to the next image by clicking 'Next' or pressing 'n' on the
keyboard (provided the Innotater has focus).

::

    import pandas as pd
    df = pd.DataFrame(targets, columns=['x','y','w','h'])
    df.to_csv('./bounding_boxes.csv', index=False)

The above saves your work - the bounding boxes you've drawn - as a CSV
file. Without saving, your numbers will be lost if the kernel restarts.

Multi-Classification of Images
++++++++++++++++++++++++++++++

Load some images from filenames in an array, initialise empty targets.

Then set up Innotater to display the images so you can mark the classes.

::

    from jupyter_innotater import *

    import numpy as np, os, cv2

    classes = ['vegetable', 'biscuit', 'fruit']
    foods = [cv2.imread('./foods/'+f) for f in os.listdir('./foods/')]
    targets = [0] * len(foods)

    Innotater( ImageInnotation(foods), MultiClassInnotation(targets, classes=classes) )

.. figure:: ../../_static/screenshots/ImageAndMultiClassifier.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter

The widget allows you to interactively step through the images selecting
the classification, and the ``targets`` variable is always kept in sync
with your changes.

Binary-Classification with Bounding Boxes for Images
++++++++++++++++++++++++++++++++++++++++++++++++++++

Set up Innotater to display the images so you can mark whether it is the
object you are trying to detect, and draw bounding boxes if so.

::

    from jupyter_innotater import *

    import numpy as np, os

    images = os.listdir('./foods/')
    bboxes = np.zeros((len(images),4), dtype='int')
    isfruits = np.ones((len(images),1), dtype='int')

    Innotater(
            ImageInnotation(images, name='Food', path='./foods'),
            [ BinaryClassInnotation(isfruits, name='Is Fruit'),
              BoundingBoxInnotation(bboxes, name='bbs', source='Food', desc='Food Type') ]
    )

.. figure:: ../../_static/screenshots/MultiClassifierAndBBoxes.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter

The widget allows you to interactively step through the images selecting
the classification, and both ``isfruits`` and ``bboxes`` are always kept
in sync with your changes.

::

    result = np.concatenate([isfruits,bboxes], axis=-1); result

Output:

::

    array([[  1, 173,  41, 135, 144],
           [  1, 138, 130,  79,  75],
           [  0,   0,   0,   0,   0],
           [  0,   0,   0,   0,   0],
           [  0,   0,   0,   0,   0],
           [  1, 205, 108,  62,  47],
           [  1, 117, 129, 158, 131],
           [  0,   0,   0,   0,   0]])

Multi-Classification of Text Strings
++++++++++++++++++++++++++++++++++++

Load some text strings e.g. of movie reviews

Set up Innotater to display the reviews so you can mark their sentiment
as positive, negative, or neutral.

::

    from jupyter_innotater import *

    reviews = ['I really liked this movie', 'It was OK', 'Do not watch!']
    sentiments = [1] * len(reviews)
    sentiment_classes = ['0 - Positive', '1 - Neutral', '2 - Negative']

    Innotater(TextInnotation(reviews), MultiClassInnotation(sentiments, classes=sentiment_classes))

.. figure:: ../../_static/screenshots/TextAndMultiClassifier.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter

The widget allows you to interactively step through the reviews
selecting the classification, and the ``sentiments`` variable is always
kept in sync.


