import sys
from pathlib import Path
import json

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

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]
