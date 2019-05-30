from .innotaterwidget import *
from .__meta__ import __version__

from .data import *
from .combine import *

__all__ = ['GroupedInnotation', 'RepeatInnotation'] \
          + ['ImageInnotation', 'BoundingBoxInnotation', 'MultiClassInnotation', 'BinaryClassInnotation', 'TextInnotation'] \
          + ['Innotater']

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-innotater',
        'require': 'jupyter-innotater/extension'
    }]
