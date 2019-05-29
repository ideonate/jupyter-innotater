import ipywidgets as widgets
from ipywidgets import HBox, VBox, IntSlider, Button, Checkbox
from traitlets import Int, observe, Unicode, Bool
from .manager import DataManager


@widgets.register
class Innotater(VBox):
    _view_name = Unicode('InnotaterView').tag(sync=True)
    _model_name = Unicode('InnotaterModel').tag(sync=True)
    _view_module = Unicode('jupyter-innotater').tag(sync=True)
    _model_module = Unicode('jupyter-innotater').tag(sync=True)
    _view_module_version = Unicode('~0.1.0').tag(sync=True)
    _model_module_version = Unicode('~0.1.0').tag(sync=True)

    index = Int().tag(sync=True)
    keyboard_shortcuts = Bool(False).tag(sync=True)

    def __init__(self, inputs, targets, indexes=None, keyboard_shortcuts=True):

        self.path = ''

        self.datamanager = DataManager(inputs, targets, indexes)

        slider = IntSlider(min=0, max=0)

        self.slider = slider

        self.prevbtn = Button(description='< Previous')
        self.nextbtn = Button(description='Next >')

        self.input_widgets = [dw.get_widget() for dw in self.datamanager.get_inputs()]
        self.target_widgets = [dw.get_widget() for dw in self.datamanager.get_targets()]

        self.add_class('innotater-base')

        controlbar_widget = HBox([self.prevbtn, slider, self.nextbtn])
        controlbar_widget.add_class('innotater-controlbar')

        super().__init__([HBox([VBox(self.input_widgets), VBox(self.target_widgets)]),
                          controlbar_widget])

        widgets.jslink((slider, 'value'), (self, 'index'))

        for dw in self.datamanager.get_targets():
            dw.widget_observe(self.update_data, names='value')
            if dw.has_children_changed_notifier:
                dw.on_children_changed(self.new_children_handler)

        for dw in list(self.datamanager.get_all()):
            dw.post_widget_create(self.datamanager)

        self.prevbtn.on_click(lambda c: self.move_slider(-1))
        self.nextbtn.on_click(lambda c: self.move_slider(1))

        self.slider.max = self.datamanager.get_data_len()-1

        self.index = 0
        self.keyboard_shortcuts = keyboard_shortcuts

        self.on_msg(self.handle_message)

        self.suspend_observed_changes = False
        self.update_ui()

    @observe('index')
    def slider_changed(self, change):
        self.update_ui()

    def move_slider(self, change):
        if change < 0 < self.index:
            self.index -= 1
        elif change > 0 and self.index < self.datamanager.get_data_len()-1:
            self.index += 1

    def handle_message(self, _, content, buffers):
        if content['event'] == 'keypress':
            code = content['code']
            self.handle_keypress(code)

    def handle_keypress(self, code):
        if self.suspend_observed_changes:
            return
        if code == 110: # n
            self.move_slider(1)
        elif code == 112: # p
            self.move_slider(-1)

    def update_ui(self):
        uindex = self.datamanager.get_underlying_index(self.index)

        self.suspend_observed_changes = True

        for dw in self.datamanager.get_all():
            dw.update_ui(uindex)

        self.suspend_observed_changes = False

        self.prevbtn.disabled = self.index <= 0
        self.nextbtn.disabled = self.index >= self.datamanager.get_data_len()-1

    def update_data(self, change):
        if self.suspend_observed_changes:
            return

        uindex = self.datamanager.get_underlying_index(self.index)
        # Find the Innotation that contains the widget that observed the change
        widg = change['owner']
        for dw in self.datamanager.get_targets():
            if dw.contains_widget(widg):
                dw.update_data(uindex)

    def add_innotations(self, inputs, targets):
        self.datamanager.dynamic_add_innotations(inputs, targets)

        for dw in targets:
            dw.widget_observe(self.update_data, names='value')
            if dw.has_children_changed_notifier:
                dw.on_children_changed(self.new_children_handler)

        for dw in inputs+targets:
            dw.post_widget_create(self.datamanager)

    def new_children_handler(self, parent, newchildren):
        self.add_innotations([], newchildren)  # Assume always targets
        self.update_ui()
