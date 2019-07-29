import ipywidgets as widgets
from traitlets import Unicode, Int, List, Bool, Dict
from .__meta__ import semver_range


@widgets.register
class ImagePad(widgets.Image):
    _view_name = Unicode('InnotaterImagePadView').tag(sync=True)
    _model_name = Unicode('InnotaterImagePadModel').tag(sync=True)
    _view_module = Unicode('jupyter-innotater').tag(sync=True)
    _model_module = Unicode('jupyter-innotater').tag(sync=True)
    _view_module_version = Unicode(semver_range).tag(sync=True)
    _model_module_version = Unicode(semver_range).tag(sync=True)

    rects = List(trait=Int).tag(sync=True)
    rect_index = Int(0).tag(sync=True)
    max_repeats = Int(0).tag(sync=True)

    wantwidth = Int(0).tag(sync=True)
    wantheight = Int(0).tag(sync=True)

    annotation_styles = Dict({}).tag(sync=True)

    is_bb_source = Bool(False).tag(sync=True)

    def setRect(self, repeat_index, x,y,w,h):
        if repeat_index == -1:
            repeat_index = 0

        r = [int(a) for a in self.rects]

        while len(r) < (repeat_index+1)*4:
            r.extend([0,0,0,0])

        r[repeat_index*4] = int(x)
        r[repeat_index*4+1] = int(y)
        r[repeat_index*4+2] = int(w)
        r[repeat_index*4+3] = int(h)

        self.rects  = r

    def set_max_repeats(self, max_repeats):
        self.max_repeats = max_repeats
        self.is_bb_source = True
