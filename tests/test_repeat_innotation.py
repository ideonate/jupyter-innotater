from jupyter_innotater import RepeatInnotation
from jupyter_innotater.data import BoundingBoxInnotation, MultiClassInnotation, TextInnotation
import ipywidgets
import numpy as np 


class TestRepeatInnotation:
    def test_constructor(self):
        classes = ['a', 'b']
        num_repeats = 4
        num_samples = 10
        RepeatInnotation(
            (
                MultiClassInnotation, 
                np.zeros((num_samples, num_repeats, len(classes)), dtype='int'), 
                dict(name='Type', classes=classes, dropdown=True, layout=ipywidgets.Layout(width='150px'))
            ),(
                BoundingBoxInnotation, 
                np.zeros((num_samples, num_repeats, 4), dtype='int'),
                {'layout': ipywidgets.Layout(width='175px')}
            ),(
                TextInnotation, 
                np.zeros((num_samples, num_repeats, len(classes)), dtype=str), 
                {'layout': ipywidgets.Layout(width='40px'), 'multiline': False}
            ),
            max_repeats=num_repeats,
            min_repeats=num_repeats,
            layout='50%'
        )