import ipywidgets as widgets
from traitlets import Unicode, Float, List

@widgets.register
class DrawingPad(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('DrawingView').tag(sync=True)
    _model_name = Unicode('DrawingModel').tag(sync=True)
    _view_module = Unicode('jupyter-innotater').tag(sync=True)
    _model_module = Unicode('jupyter-innotater').tag(sync=True)
    _view_module_version = Unicode('~0.1.0').tag(sync=True)
    _model_module_version = Unicode('~0.1.0').tag(sync=True)
    value = Unicode('Hello World!!!!!!!!!!!!!!!!').tag(sync=True)
    # data_x = List([]).tag(sync=True)
    # data_y = List([]).tag(sync=True)
    # time = List([]).tag(sync=True)
    data = List([[],[],[]]).tag(sync=True)

    def clear(self):
        self.data = [[], [], []]


