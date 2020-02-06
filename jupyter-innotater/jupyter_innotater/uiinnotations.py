__all__ = ['ButtonInnotation']

from ipywidgets import Button

from .data import Innotation
from .mixins import DataChangeNotifierMixin


class ButtonInnotation(Innotation, DataChangeNotifierMixin):
    """
    Allow embedding of an arbitrary widget object, e.g. for text display
    Must still have a data attribute of correct len, even if dummy values
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_click_hook = kwargs.get('on_click', None)
        self.uindex = None

    def _create_widget(self):
        btn = Button(description=self.desc, disabled=self.disabled, layout=self.layout)
        if self.on_click_hook:
            btn.on_click(lambda b: self.call_on_click_hook(b))
        return btn

    def call_on_click_hook(self, b):
        och = self.on_click_hook
        changed = och(self.uindex, self.repeat_index, name=self.name, desc=self.desc)
        if changed:
            self.data_changed()

    def update_ui(self, uindex):
        self.uindex = uindex

    def update_data(self, uindex):
        pass
