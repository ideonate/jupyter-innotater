import ipywidgets as widgets
from ipywidgets import HBox, VBox, IntSlider, Button
from traitlets import Int, observe, Unicode, Bool

from .manager import DataManager
from .__meta__ import semver_range
from .mixins import ChildrenChangeNotifierMixin, DataChangeNotifierMixin

@widgets.register
class Innotater(VBox):  #VBox
    _view_name = Unicode('InnotaterView').tag(sync=True)
    _model_name = Unicode('InnotaterModel').tag(sync=True)
    _view_module = Unicode('jupyter-innotater').tag(sync=True)
    _model_module = Unicode('jupyter-innotater').tag(sync=True)
    _view_module_version = Unicode(semver_range).tag(sync=True)
    _model_module_version = Unicode(semver_range).tag(sync=True)

    index = Int().tag(sync=True)
    keyboard_shortcuts = Bool(False).tag(sync=True)
    is_dirty = Bool(False).tag(sync=True)

    def __init__(self, inputs, targets, indexes=None, keyboard_shortcuts=True, save_hook=None):

        self.path = ''

        self.dirty_uindexes = set()

        self.save_hook = save_hook

        self.datamanager = DataManager(inputs, targets, indexes)

        slider = IntSlider(min=0, max=0)

        self.slider = slider

        self.prevbtn = Button(description='< Previous')
        self.nextbtn = Button(description='Next >')

        self.input_widgets = [dw.get_widget() for dw in self.datamanager.get_inputs()]
        self.target_widgets = [dw.get_widget() for dw in self.datamanager.get_targets()]

        self.add_class('innotater-base')

        cbar_widgets = [self.prevbtn, slider, self.nextbtn]
        if self.save_hook:
            self.savebtn = Button(description='Save', disabled=True)
            cbar_widgets.append(self.savebtn)

        controlbar_widget = HBox(cbar_widgets)
        controlbar_widget.add_class('innotater-controlbar')

        super().__init__([HBox([VBox(self.input_widgets), VBox(self.target_widgets)]),
                          controlbar_widget])

        widgets.jslink((slider, 'value'), (self, 'index'))

        self._observe_targets(self.datamanager.get_targets())

        for dw in list(self.datamanager.get_all()):
            dw.post_widget_create(self.datamanager)

        self.prevbtn.on_click(lambda c: self.move_slider(-1))
        self.nextbtn.on_click(lambda c: self.move_slider(1))

        if self.save_hook:
            self.savebtn.on_click(lambda c: self.save_hook_fire())

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
        if content['event'] == 'keydown':
            code = content['code']
            self.handle_keypress(code)

    def handle_keypress(self, code):
        if self.suspend_observed_changes:
            return
        if code == 78: # n was 110
            self.move_slider(1)
        elif code == 80: # p was 112
            self.move_slider(-1)
        elif code == 83: # s
            self.save_hook_fire()

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

        self._make_dirty(uindex)

    def _make_dirty(self, uindex):
        self.dirty_uindexes.add(uindex)

        if self.save_hook and not self.is_dirty:
            self.is_dirty = True
            self.savebtn.disabled = not self.is_dirty

    def save_hook_fire(self):
        if self.save_hook:
            self.savebtn.disabled = True # Disable during save
            has_saved = self.save_hook(list(self.dirty_uindexes))
            if has_saved:
                self.is_dirty = False
                self.dirty_uindexes.clear()
            self.savebtn.disabled = not self.is_dirty

    def add_innotations(self, inputs, targets):
        self.datamanager.dynamic_add_innotations(inputs, targets)
        self._observe_targets(targets)
        for dw in inputs+targets:
            dw.post_widget_create(self.datamanager)

    def _observe_targets(self, targets):
        for dw in targets:
            dw.widget_observe(self.update_data, names='value')
            if isinstance(dw, ChildrenChangeNotifierMixin):
                dw.on_children_changed(self.new_children_handler)
            if isinstance(dw, DataChangeNotifierMixin):
                dw.on_data_changed(self.updated_data_handler)

    def new_children_handler(self, parent, newchildren):
        self.add_innotations([], newchildren)  # Assume always targets
        self.update_ui()

    def updated_data_handler(self, widget):
        uindex = self.datamanager.get_underlying_index(self.index)
        self._make_dirty(uindex)
        self.update_ui()
