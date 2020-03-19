__all__ = ['GroupedInnotation', 'RepeatInnotation']

from ipywidgets import HBox, VBox, Button

from .data import Innotation
from .mixins import ChildrenChangeNotifierMixin


class GroupedInnotation(Innotation):

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs)

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

    def list_innotations_tree(self):
        return [self, *self.childinnotations]

    def __len__(self):
        if len(self.childinnotations) > 0:
            return len(self.childinnotations[0])
        return 0


class RepeatInnotation(Innotation, ChildrenChangeNotifierMixin):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.rows_count = 0

        self.childinnotationconfigs = args

        self.childinnotations = []

        self.min_repeats = kwargs.get('min_repeats', 0)
        self.max_repeats = kwargs.get('max_repeats', 10)

        if self.max_repeats < self.min_repeats:
            raise Exception("min_repeats is greater than max_repeats")

    def post_widget_create(self, datamanager):
        while self.rows_count < self.min_repeats:
            self.add_row()

    def _create_widget(self):
        self.addbtn = Button(description='Add')
        self.addbtn.on_click(self.add_row_handler)
        vbox = VBox([self.addbtn])
        vbox.add_class('repeat-innotation')
        return vbox

    def add_row_handler(self, btn):
        self.add_row()

    def add_row(self):
        newchildren = []
        for c in self.childinnotationconfigs:
            if isinstance(c, tuple) or isinstance(c, list):
                kwargs = {} if len(c) <= 2 else c[2]

                kwargs['repeat_index'] = self.rows_count
                if 'name' in kwargs:
                    kwargs['name'] = '{}_{}'.format(kwargs['name'], self.rows_count)
                newchildren.append(c[0](c[1], **kwargs))
            else:
                newchildren.append(c(self.data))

        self.rows_count += 1
        self.children_changed(newchildren)

        self.get_widget().children = tuple(list(self.get_widget().children)+[HBox([c.get_widget() for c in newchildren])])

        self.childinnotations.extend(newchildren)

        if self.max_repeats == self.rows_count:
            self.addbtn.disabled = True

    def update_ui(self, uindex):
        for innot in self.childinnotations:
            innot.update_ui(uindex)

    def update_data(self, uindex):
        for innot in self.childinnotations:
            innot.update_data(uindex)
