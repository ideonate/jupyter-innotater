from .imagewidget import ImagePad
from ipywidgets import Checkbox, Select, Text, Textarea, Dropdown
import re
from pathlib import Path


class Innotation:

    anonindex = 1

    def __init__(self, *args, **kwargs):

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'data{}'.format(Innotation.anonindex)
            Innotation.anonindex += 1

        self.desc = kwargs.get('desc', self.name)

        if len(args) > 0:
            self.data = args[0]
            if 'data' in kwargs:
                raise Exception('data supplied both as position and keyword argument')
        elif 'data' in kwargs:
            self.data = kwargs['data']
        else:
            raise Exception('No data argument found')

        self.widget = None

        self.layout = kwargs.get('layout', {})

        if 'disabled' in kwargs:
            self.disabled = kwargs['disabled']

    def get_name(self):
        return self.name

    def post_register(self, datamanager):
        if not hasattr(self, 'disabled'):
            self.disabled = datamanager.is_input(self)

    def post_widget_create(self, datamanager):
        pass

    def __len__(self):
        return len(self.data)

    def get_widget(self):
        if self.widget is None:
            self.widget = self._create_widget() # on derived class
        return self.widget

    def _get_widget_value(self):
        return self.get_widget().value

    def update_ui(self, uindex):
        raise Exception('Do not call update_ui on base class')

    def update_data(self, uindex):
        raise Exception('Do not call update_data on an input-only class')


class ImageInnotation(Innotation):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.path = kwargs.get('path', '')

        self.transform = kwargs.get('transform', None)

    def _create_widget(self):
        return ImagePad(wantwidth=self.width, wantheight=self.height, layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        if self.transform is None:
            it = self.data[uindex]
        else:
            it = self.transform(self.data[uindex])

        if hasattr(self.data[uindex], '__fspath__') or isinstance(self.data[uindex], str):
            # Path-like
            p = Path(it)
            if self.path != '':
                p = Path(self.path) / p
            self.get_widget().set_value_from_file(p)
        elif 'numpy' in str(type(it)) or 'Tensor' in str(type(it)):
            import cv2, numpy as np # Required to manipulate numpy or pytorch image matrix
            npim = it.numpy() if hasattr(it, 'numpy') else it
            if len(npim.shape) == 3 and npim.shape[2] not in (1,3,4):
                # Channels dim needs to be moved to back
                npim = npim.transpose((1,2,0))
            if not np.issubdtype(npim.dtype, np.integer):
                # Float so scale
                npim = (npim * 255).astype('int')
            self.get_widget().value = cv2.imencode('.png', npim)[1].tostring()
        else:
            # Actual raw image data
            self.get_widget().value = it

    def setRect(self, x,y,w,h):
        self.get_widget().setRect(x,y,w,h)


class BoundingBoxInnotation(Innotation):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.source = kwargs.get('source', None)
        self.sourcedw = None

    def post_register(self, datamanager):
        if self.source is not None:
            self.sourcedw = datamanager.get_data_wrapper_by_name(self.source)

            if self.sourcedw is None:
                raise Exception(f'ImageInnotation named {self.source} not found but specified as source attribute for BoundingBoxInnotation')

            if not isinstance(self.sourcedw, ImageInnotation):
                raise Exception(f'Innotation named {self.source} is not an ImageInnotation but is specified as source attribute for BoundingBoxInnotation')

        else:
            # Find by type
            dws = datamanager.get_data_wrappers_by_type(ImageInnotation)
            if len(dws) != 1:
                # Raises exception if 0 or >1 of these is found
                raise Exception(f'ImageInnotation not found uniquely')

            self.sourcedw = dws[0]

        super().post_register(datamanager)

    def post_widget_create(self, datamanager):
        if self.sourcedw is not None:
            self.sourcedw.get_widget().is_bb_source = True
            self.sourcedw.get_widget().observe(self.rectChanged, names='rect')

    def _create_widget(self):
        return Text(layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        self.get_widget().value = self._value_to_str(self.data[uindex])
        self._sync_to_image(uindex)

    def _sync_to_image(self, uindex):
        if self.sourcedw is not None:
            (x,y,w,h) = self.data[uindex][:4]
            self.sourcedw.setRect(x,y,w,h)

    def _value_to_str(self, r):
        return ', '.join([str(int(a)) for a in r])

    def update_data(self, uindex):
        newval = self.get_widget().value
        if newval != self._value_to_str(self.data[uindex]):
            try:
                self.data[uindex] = [int(float(s)) for s in re.split('[ ,]+', newval)]
                self._sync_to_image(uindex)
            except ValueError:
                pass

    def rectChanged(self, change):
        if self.sourcedw is not None:
            r = self.sourcedw.get_widget().rect
            self.get_widget().value = self._value_to_str(r)


class MultiClassInnotation(Innotation):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Just a 1-dim array with values corresponding to class numbers e.g. 0-5
        self.datadepth = 'simple'

        self.dims = 1
        if hasattr(self.data[0], '__len__'):
            self.dims = 2

        if self.dims > 1:
            if len(self.data[0]) == 1:
                self.datadepth = 'colvector' # A column vector corresponding to class numbers directly
            else:
                self.datadepth = 'onehot' # One-hot encoding
                #a = np.unique(np.array(self.data))
                #if len(a) > 2:
                #    raise Exception('data looks like onehot but does not just contain 0s and 1s')

        if 'classes' in kwargs:
            self.classes = kwargs['classes']
        else:
            # Guess the range of classes
            self._guess_classes()

        self.dropdown = kwargs.get('dropdown', False)

    def _guess_classes(self):
        if self.datadepth == 'onehot':
            m = len(self.data[0])-1
        elif self.datadepth == 'simple':
            m = max(self.data)
        else: # colvector
            m = max(self.data)[0]

        if m == 0:
            raise Exception(f'MultiClassInnotation {self.name} only has one class value in use so cannot infer class count - please specify a classes array')

        self.classes = [str(i) for i in range(m+1)]

    def _create_widget(self):
        if self.dropdown:
            return Dropdown(options=self.classes, layout=self.layout, disabled=self.disabled)
        return Select(options=self.classes, layout=self.layout, disabled=self.disabled)

    def _calc_class_index(self, uindex):
        if self.datadepth == 'onehot':
            return int(max(range(len(self.data[uindex])), key=lambda x: self.data[uindex][x], default=0))
        if self.datadepth == 'simple':
            return int(self.data[uindex])
        # colvector
        return int(self.data[uindex][0])

    def update_ui(self, uindex):
        self.get_widget().value = self.classes[self._calc_class_index(uindex)]

    def update_data(self, uindex):
        newval = self._get_widget_value()
        old_class_index = self._calc_class_index(uindex)
        if newval != self.classes[old_class_index]:
            class_index = self.classes.index(newval)
            if self.datadepth == 'onehot':
                self.data[uindex][old_class_index] = 0
                self.data[uindex][class_index] = 1
            elif self.datadepth == 'simple':
                self.data[uindex] = class_index
            else:
                # colvector
                self.data[uindex][0] = class_index


class BinaryClassInnotation(MultiClassInnotation):

    def _guess_classes(self):
        self.classes = ['False', 'True']

    def _create_widget(self):
        return Checkbox(description=self.desc, layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        self.get_widget().value = bool(self._calc_class_index(uindex) == 1)

    def _get_widget_value(self):
        return self.classes[self.get_widget().value and 1 or 0]


class TextInnotation(Innotation):

    def _create_widget(self):
        return Textarea(layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        self.get_widget().value = str(self.data[uindex])

    def update_data(self, uindex):
        newval = str(self._get_widget_value())
        if newval != str(self.data[uindex]):
            self.data[uindex] = newval


class _WidgetInnotation(Innotation):
    """
    Allow embeding of an arbitrary widget object, e.g. for text display
    Must still have a data attribute of correct len, even if dummy values
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if 'widget' not in kwargs:
            raise Exception(f'{self.__class__} requires a widget argument')
        self.widget = kwargs['widget']

    def _create_widget(self):
        return self.widget

    def update_ui(self, uindex):
        pass

    def update_data(self, uindex):
        pass
