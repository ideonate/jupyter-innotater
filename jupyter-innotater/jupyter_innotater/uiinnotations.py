__all__ = ['ButtonInnotation']

from .data import Innotation
from ipywidgets import Button
from ipywidgets.widgets import CallbackDispatcher


class ButtonInnotation(Innotation):
    """
    Allow embeding of an arbitrary widget object, e.g. for text display
    Must still have a data attribute of correct len, even if dummy values
    """

    requires_data = False
    has_data_changed_notifier = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_click_hook = kwargs.get('on_click', None)
        self.uindex = None
        self._data_changed_handlers = CallbackDispatcher()

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

    def on_data_changed(self, callback, remove=False):
        """Register a callback to execute when the children are changed.

        The callback will be called with one argument, this Innotation
        winstance.

        Parameters
        ----------
        remove: bool (optional)
            Set to true to remove the callback from the list of callbacks.
        """
        self._data_changed_handlers.register_callback(callback, remove=remove)

    def data_changed(self):
        """Programmatically trigger a click event.

        This will call the callbacks registered to the clicked button
        widget instance.
        """
        self._data_changed_handlers(self)
