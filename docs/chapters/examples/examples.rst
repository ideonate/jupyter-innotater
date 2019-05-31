Examples
--------

Documentation for examples is divided into two main sections: 'single' examples where the Innotation objects are used
directly; and 'multiple' examples where we introduce the RepeatInnotation class which allows you to specify arbitrary
numbers of the same ordinary-Innotation (e.g. 10 bounding boxes). Note it is possible, and sometimes easier, to specify
multiple Bounding Boxes using the 'single' method but can become cumbersome for large numbers.

The single and multiple examples can be found through the links immediately below. At the bottom of this document are
instructions for running similar examples interactively in Jupyter notebooks, and also for a tutorial showing an
example end-to-end project including motivation for drawing bounding boxes.

.. toctree::
   :maxdepth: 3
   :caption: Examples:

   single
   multiple


Jupyter Notebook Examples
+++++++++++++++++++++++++

The Jupyter Notebooks in the Example folder of the git repository contain many examples you can run
directly in Jupyter notebook. You can try it out for free in a
`Binder <https://mybinder.org/>`__ environment by clicking here:
`Examples.ipynb on
Binder <https://mybinder.org/v2/gh/ideonate/jupyter-innotater/master>`__

For the full effect in your own environment, you may need to install
opencv2 and pandas packages (or just ignore those parts of the
notebook):

::

    pip install jupyter_innotater
    pip install opencv-python
    pip install pandas

Full Tutorial of an example project
+++++++++++++++++++++++++++++++++++

An example machine learning project for butterfly species classification
using bounding boxes to improve the model by zooming in: `Clean Up your
own Model Data without leaving
Jupyter <https://towardsdatascience.com/clean-up-your-own-model-data-without-leaving-jupyter-bdbcc9001734>`__

