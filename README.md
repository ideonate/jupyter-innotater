# jupyter-innotater

Annotate data including image bounding boxes inline within your [Jupyter notebook](https://jupyter.org/) in Python. Innotater's flexible API allows easy selection of interactive controls to suit your datasets exactly. 

Now works with JupyterLab (2.0+ recommended)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ideonate/jupyter-innotater/master)

[![Documentation Status](https://readthedocs.org/projects/jupyter-innotater/badge/?version=latest)](https://jupyter-innotater.readthedocs.io/en/latest/?badge=latest)

## 1 - Overview

In a data science or machine learning project, you may prepare and study images or other data within a Jupyter notebook then need to annotate the data to augment the training or fix errors in your source data.

Since you are already working within a Jupyter notebook, the Innotater works inline allowing you to interact with your data and annotate it quickly and easily, syncing straight back to your input data arrays or matrices.

Within Jupyter, you can easily home in on problem input data - perhaps only misclassified images - so you can step through and adjust bounding boxes just for those items. 

The Innotater widget is designed with a flexible API making it quick and easy to get started exploring your dataset, guessing how to work with your data without explicit configuration where possible.

The project is currently in ALPHA development phase, and I appreciate all feedback on any problems including details on how the current code works or fails to work for the structure of your particular projects.

**Full documentation is [now on ReadTheDocs](https://jupyter-innotater.readthedocs.io/)**

## 2 - Examples

You can easily combine Innotater's interactive components to suit your project. Here are some examples.

### Images and Bounding Boxes

Load some images from filenames in an array, initialise empty bounding boxes.

Then set up Innotater to display the images so you can draw updated bounding boxes directly.

```python
from jupyter_innotater import *
import numpy as np, os

images = os.listdir('./foods/')
targets = np.zeros((len(images), 4)) # Initialise bounding boxes as x,y = 0,0, width,height = 0,0

Innotater( ImageInnotation(images, path='./foods'), BoundingBoxInnotation(targets) )
```

![Screenshot of Innotater widget in Jupyter](docs/_static/screenshots/ImageAndBBoxesInnotater.png)

The widget allows you to interactively draw bounding boxes for any of the images, and the `targets` variable is always kept in sync with your changes.

Advance to the next image by clicking 'Next' or pressing 'n' on the keyboard (provided the Innotater has focus).

```python
import pandas as pd
df = pd.DataFrame(targets, columns=['x','y','w','h'])
df.to_csv('./bounding_boxes.csv', index=False)
```

The above saves your work - the bounding boxes you've drawn - as a CSV file. Without saving, your numbers will be lost if the kernel restarts.


### Multi-Classification of Text Strings

Load some text strings e.g. of movie reviews

Set up Innotater to display the reviews so you can mark their sentiment as positive, negative, or neutral.

Use `indexes` parameter to display only the reviews we want to check.

```python
from jupyter_innotater import *

reviews = ['I really liked this movie', 'It was OK', 'Do not watch!', 'Ignore me']
sentiments = [1] * len(reviews)
sentiment_classes = ['0 - Positive', '1 - Neutral', '2 - Negative']

Innotater(
    TextInnotation(reviews), 
    MultiClassInnotation(sentiments, classes=sentiment_classes),
    indexes=[0,1,2]
)
```

![Screenshot of Innotater widget in Jupyter](docs/_static/screenshots/TextAndMultiClassifier.png)

The widget allows you to interactively step through the reviews selecting the classification, and the `sentiments` variable is always kept in sync.


### Multiple Bounding Boxes and Multi-classification 

For each photo, draw multiple bounding boxes and specify for each bounding box what is depicted (from a dropdown).

There is also an 'Exclude' checkbox per photo so we can select if that photo should be excluded from the dataset - you would write some code to remove those before full processing later on.

Also display the filename in a textbox, for information only.

```python
from jupyter_innotater import *
import numpy as np, os

animalfns = sorted(os.listdir('./animals/'))

repeats = 4

# Per-photo data
targets_exclude = np.zeros((len(animalfns), 1), dtype='int') # Binary flag to indicate want to exclude from dataset

# Repeats within each photo
breeds = ['Cat - Shorthair tabby', 'Cat - Shorthair ginger', 'Dog - Labrador', 'Dog - Beagle', 'Dog - Terrier']
targets_breed = np.zeros((len(animalfns), len(breeds)), dtype='int')
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
```

![Screenshot of Innotater widget in Jupyter](docs/_static/screenshots/MultipleBBoxesANDMultiClass.png)


### Jupyter Notebook Examples

The notebooks in the Example folder contain many examples you can run directly in Jupyter notebook. You can try them out for free in a [Binder](https://mybinder.org/) environment by clicking here: [Innotater on Binder](https://mybinder.org/v2/gh/ideonate/jupyter-innotater/master)


## 3 - Installation

### Install from PyPi (recommended)

```
pip install jupyter_innotater
```

To enable in JupyterLab (version 2.0+ recommended):

```
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-innotater
```
   
## 4 - Contact for Feedback

Please get in touch with any feedback or questions: [dan@ideonate.com](dan@ideonate.com). It will be especially useful to understand the structure of your project and what is needed to augment your data - e.g. extra shape types. There are many ideas on the roadmap, and your input is vital for prioritising these.

## 5 - License

This code is released under an MIT license.

## 6 - Documentation

Full documentation is now on ReadTheDocs:
* [Stable version as installed through pip](https://jupyter-innotater.readthedocs.io/en/stable/index.html)
* [Latest version in development](https://jupyter-innotater.readthedocs.io/en/latest/index.html)
