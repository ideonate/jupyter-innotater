import ipywidgets as widgets
from ipywidgets.widgets import CallbackDispatcher
from traitlets import Unicode
from .__meta__ import semver_range


@widgets.register
class FocusText(widgets.Text):
    _view_name = Unicode('FocusTextView').tag(sync=True)
    _view_module = Unicode('jupyter-innotater').tag(sync=True)
    _view_module_version = Unicode(semver_range).tag(sync=True)

    def __init__(self, **kwargs):
        super(FocusText, self).__init__(**kwargs)
        self._click_handlers = CallbackDispatcher()
        self.on_msg(self._handle_focustext_msg)

    def on_click(self, callback, remove=False):
        """Register a callback to execute when the button is clicked.

        The callback will be called with one argument, the clicked button
        widget instance.

        Parameters
        ----------
        remove: bool (optional)
            Set to true to remove the callback from the list of callbacks.
        """
        self._click_handlers.register_callback(callback, remove=remove)

    def click(self):
        """Programmatically trigger a click event.

        This will call the callbacks registered to the clicked button
        widget instance.
        """
        self._click_handlers(self)

    def _handle_focustext_msg(self, _, content, buffers):
        """Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
            Content of the msg.
        """
        if content.get('event', '') == 'click':
            self.click()
