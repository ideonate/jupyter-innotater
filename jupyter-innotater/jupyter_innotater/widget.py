import ipywidgets as widgets
from ipywidgets import HBox, VBox, IntSlider, Checkbox, Button
from traitlets import Int, observe
from .manager import DataManager

@widgets.register
class Innotater(VBox):
    #_view_name = Unicode('InnotaterView').tag(sync=True)
    #_model_name = Unicode('InnotaterModel').tag(sync=True)
    #_view_module = Unicode('jupyter-innotater').tag(sync=True)
    #_model_module = Unicode('jupyter-innotater').tag(sync=True)
    #_view_module_version = Unicode('~0.1.0').tag(sync=True)
    #_model_module_version = Unicode('~0.1.0').tag(sync=True)

    index = Int().tag(sync=True)

    def __init__(self, inputs, targets):

        self.path = ''

        self.datamanager = DataManager(inputs, targets)

        slider = IntSlider(min=0, max=0)

        self.slider = slider

        self.prevbtn = Button(description='< Previous')
        self.nextbtn = Button(description='Next >')

        self.input_widgets = [dw.get_widget() for dw in self.datamanager.get_inputs()]
        self.target_widgets = [dw.get_widget() for dw in self.datamanager.get_targets()]

        super().__init__([HBox([VBox(self.input_widgets), VBox(self.target_widgets)]), HBox([self.prevbtn, slider, self.nextbtn])])

        jsl = widgets.jslink((slider, 'value'), (self, 'index'))

        for dw in self.datamanager.get_targets():
            dw.get_widget().observe(self.update_data, names='value')

        for dw in self.datamanager.get_all():
            dw.post_widget_create(self.datamanager)

        self.prevbtn.on_click(lambda c: self.move_slider(-1))
        self.nextbtn.on_click(lambda c: self.move_slider(1))


        self.slider.max = self.datamanager.get_data_len()-1
        self.index = 0
        self.update_ui()


    @observe('index')
    def slider_changed(self, change):
        self.update_ui()

    def move_slider(self, change):
        if change < 0 < self.index:
            self.index -= 1
        elif change > 0 and self.index < self.datamanager.get_data_len()-1:
            self.index += 1

    def update_ui(self):
        i = self.index

        for dw in self.datamanager.get_all():
            dw.update_ui(i)

        self.prevbtn.disabled = self.index <= 0
        self.nextbtn.disabled = self.index >= self.datamanager.get_data_len()-1

    def update_data(self, change):
        # Find the DataWrapper that contains the widget that observed the change
        widg = change['owner']
        for dw in self.datamanager.get_targets():
            if widg == dw.get_widget():
                dw.update_data(self.index)
