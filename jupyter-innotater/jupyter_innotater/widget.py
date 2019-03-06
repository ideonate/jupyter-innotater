from .image import ImagePad
import ipywidgets as widgets
from ipywidgets import HBox, VBox, IntSlider, Checkbox, Image
from traitlets import Unicode, List, Int, Bool, observe

@widgets.register
class Innotater(VBox):
    #_view_name = Unicode('InnotaterView').tag(sync=True)
    #_model_name = Unicode('InnotaterModel').tag(sync=True)
    #_view_module = Unicode('jupyter-innotater').tag(sync=True)
    #_model_module = Unicode('jupyter-innotater').tag(sync=True)
    #_view_module_version = Unicode('~0.1.0').tag(sync=True)
    #_model_module_version = Unicode('~0.1.0').tag(sync=True)

    index = Int().tag(sync=True)
#    inputs = List().tag(sync=True)
#    path = Unicode('').tag(sync=True)
#    targets = List([]).tag(sync=True)

    def __init__(self):

        image_pad = ImagePad()

        slider = IntSlider(min=0, max=0)

        checkbox = Checkbox()

        self.image_pad = image_pad
        self.slider = slider
        self.checkbox = checkbox

        super().__init__([HBox([image_pad, checkbox]), slider])

        jsl = widgets.jslink((slider, 'value'), (self, 'index'))


        self.checkbox.observe(self.checkbox_changed, 'value')


    @observe('index')
    def slider_changed(self, change):
        self.update_ui()

    def update_ui(self):
        i = self.index
        fn = self.inputs[i]

        self.image_pad.set_value_from_file(self.path+fn)

        self.checkbox.value = self.targets[i] == 1

    def checkbox_changed(self, change):
        i = self.index
        if self.targets[i] != change['new']:
            self.targets[i] = change['new'] and 1 or 0

    def load(self, inputs, targets, path=None):
        self.inputs = inputs
        self.targets = targets
        if path is not None:
            self.path = path
        self.slider.max = len(inputs)-1
        self.index = 0
        self.update_ui()
