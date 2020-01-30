import sys
assert sys.version_info[0] >= 3, "Innotater requires Python 3.3 or above. Current Python version: " + sys.version.split(' ')[0]

from .innotaterwidget import *
from .__meta__ import __version__

from .data import *
from .combine import *
from .uiinnotations import *

__all__ = ['GroupedInnotation', 'RepeatInnotation',
           'ImageInnotation', 'BoundingBoxInnotation', 'MultiClassInnotation',
           'BinaryClassInnotation', 'TextInnotation', 'ButtonInnotation',
           'Innotater', '__version__']

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-innotater',
        'require': 'jupyter-innotater/extension'
    }]
