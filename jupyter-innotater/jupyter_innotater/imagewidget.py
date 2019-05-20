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

    # rect = List(trait=Int).tag(sync=True)
    rects = List(trait=Int).tag(sync=True)
    rect_index = Int(0).tag(sync=True)

    wantwidth = Int(0).tag(sync=True)
    wantheight = Int(0).tag(sync=True)

    is_bb_source = Bool(False).tag(sync=True)

    def setRect(self, repeat_index, x,y,w,h):
        if repeat_index != -1:
            self.rect_index = repeat_index
        else:
            repeat_index = 0

        while len(self.rects) < (repeat_index+1)*4:
            self.rects.extend([0,0,0,0])
        self.rects[repeat_index*4] = int(x)
        self.rects[repeat_index*4+1] = int(y)
        self.rects[repeat_index*4+2] = int(w)
        self.rects[repeat_index*4+3] = int(h)
