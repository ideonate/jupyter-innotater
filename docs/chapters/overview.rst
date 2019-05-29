.. _overview:

Overview
---------

In a data science or machine learning project, you may prepare and study
images or other data within a Jupyter notebook then need to annotate the
data to augment the training or fix errors in your source data. You may
need to check classifications are correct (cats/dogs correctly
specified) or add bounding boxes around the pertinent parts of your
images. For example, to build a dog breed classified you might first
build a model that learns how to identify the bounding box of a dog
within the image, then your final model zooms in on that box in order to
train/evaluate the breed classifier.

Since you are already working within a Jupyter notebook, the Innotater
works inline allowing you to interact with your data and annotate it
quickly and easily, syncing straight back to your input data arrays or
matrices.

Within Jupyter, you can easily home in on problem input data - perhaps
only misclassified images - so you can step through and adjust bounding
boxes just for those items.

The Innotater widget is designed with a flexible API making it quick and
easy to get started exploring your data, guessing how to work with your
data without explicit configuration where possible.

The widget is currently in ALPHA development phase, and I appreciate all
feedback on any problems including details on how the current code works
or fails to work for the structure of your particular projects.

.. figure:: ../_static/screenshots/ImageAndBBoxesFull.png
   :alt: Screenshot of Innotater widget in Jupyter

   Screenshot of Innotater widget in Jupyter
