from .innotaterwidget import *

from .__meta__ import __version__

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-innotater',
        'require': 'jupyter-innotater/extension'
    }]
