import ipywidgets as widgets
from traitlets import Unicode, Int, List, Bool


@widgets.register
class ImagePad(widgets.Image):
    _view_name = Unicode('InnotaterImagePadView').tag(sync=True)
    _model_name = Unicode('InnotaterImagePadModel').tag(sync=True)
    _view_module = Unicode('jupyter-innotater').tag(sync=True)
    _model_module = Unicode('jupyter-innotater').tag(sync=True)
    _view_module_version = Unicode('~0.1.0').tag(sync=True)
    _model_module_version = Unicode('~0.1.0').tag(sync=True)

    rect = List(trait=Int).tag(sync=True)

    wantwidth = Int(0).tag(sync=True)
    wantheight = Int(0).tag(sync=True)

    is_bb_source = Bool(False).tag(sync=True)

    def setRect(self,x,y,w,h):
        self.rect = [int(x),int(y),int(w),int(h)]
