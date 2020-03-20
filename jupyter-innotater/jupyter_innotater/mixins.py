from ipywidgets.widgets import CallbackDispatcher


class DataMixin:
  def __init__(self, *args, **kwargs):
    self.repeat_index = kwargs.get('repeat_index', -1)

    if len(args) > 0:
      self.data = args[0]
      if 'data' in kwargs:
        raise Exception('data supplied both as position and keyword argument')
    elif 'data' in kwargs:
      self.data = kwargs['data']
    else:
      raise Exception('No data argument found')

  def _get_data(self, uindex):
    if self.repeat_index == -1:
      return self.data[uindex]
    return self.data[uindex][self.repeat_index]

  def _set_data(self, uindex, *args):
    if len(args) < 1 or len(args) > 2:
      raise Exception("_set_data must have exactly one or two args")

    if self.repeat_index != -1:
      if len(args) == 2:
        self.data[uindex, self.repeat_index, args[0]] = args[-1]
      else:
        self.data[uindex, self.repeat_index] = args[-1]
    else:
      if len(args) == 2:
        self.data[uindex, args[0]] = args[-1]
      else:
        self.data[uindex] = args[-1]

  def __len__(self):
    return len(self.data)


class DataChangeNotifierMixin:

  def __init__(self, *args, **kwargs):
    self.repeat_index = kwargs.get('repeat_index', -1)
    self._data_changed_handlers = CallbackDispatcher()

  def on_data_changed(self, callback, remove=False):
    """Register a callback to execute when the children are changed.

    The callback will be called with one argument, this Innotation
    winstance.

    Parameters
    ----------
    callback: method handle
            Method to be registered or unregistered.
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


class ChildrenChangeNotifierMixin:

  def __init__(self, *args, **kwargs):
    self._children_changed_handlers = CallbackDispatcher()

  def on_children_changed(self, callback, remove=False):
    """Register a callback to execute when the children are changed.

    The callback will be called with one argument, this Innotation
    winstance.

    Parameters
    ----------
    callback: method handle
            Method to be registered or unregistered.
    remove: bool (optional)
        Set to true to remove the callback from the list of callbacks.
    """
    self._children_changed_handlers.register_callback(callback, remove=remove)

  def children_changed(self, newchildren):
    """Programmatically trigger a click event.

    This will call the callbacks registered to the clicked button
    widget instance.
    """
    self._children_changed_handlers(self, newchildren)