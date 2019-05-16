from .data import Innotation
from ipywidgets import HBox

class GroupedInnotation(Innotation):

    requires_data = False

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.childinnotations = args

    def post_register(self, datamanager):
        for innot in self.childinnotations:
            innot.post_register(datamanager)

    def post_widget_create(self, datamanager):
        for innot in self.childinnotations:
            innot.post_widget_create(datamanager)

    def _create_widget(self):
        return HBox([innot.get_widget() for innot in self.childinnotations])

    def _get_widget_value(self):
        raise Exception('Do not call _get_widget_value on GroupedInnotation class')

    def widget_observe(self, fn, names):
        for innot in self.childinnotations:
            innot.widget_observe(fn, names=names)

    def update_ui(self, uindex):
        for innot in self.childinnotations:
            innot.update_ui(uindex)

    def update_data(self, uindex):
        for innot in self.childinnotations:
            innot.update_data(uindex)

    def contains_widget(self, widget):
        for innot in self.childinnotations:
            if innot.contains_widget(widget):
                return True
        return False
