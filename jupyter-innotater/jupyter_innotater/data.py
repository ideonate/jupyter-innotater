__all__ = ['ImageInnotation', 'BoundingBoxInnotation', 'MultiClassInnotation', 'BinaryClassInnotation', 'TextInnotation']

from ipywidgets import Checkbox, Select, Textarea, Dropdown, Text
import re
from pathlib import Path
import numpy as np # Required to manipulate numpy or pytorch image matrix

from .imagewidget import ImagePad
from .customwidgets import FocusText
from .watchlist import Watcher, WatchList
from .mixins import DataMixin

try:
    import cv2 # Prefer Open CV2 but don't put in requirements.txt because it can be difficult to install
    usecv2 = True
except ImportError:
    import png, io # PyPNG is a pure-Python PNG manipulator
    usecv2 = False


class Innotation:

    anonindex = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'data{}'.format(Innotation.anonindex)
            Innotation.anonindex += 1

        self.desc = kwargs.get('desc', self.name)
        self.widget = None
        self.layout = kwargs.get('layout', {})
        if 'disabled' in kwargs:
            self.disabled = kwargs['disabled']

    def post_register(self, datamanager):
        if not hasattr(self, 'disabled'):
            self.disabled = datamanager.is_input(self)

    def post_widget_create(self, datamanager):
        pass

    def get_widget(self):
        if self.widget is None:
            self.widget = self._create_widget() # on derived class
        return self.widget

    def _get_widget_value(self):
        return self.get_widget().value

    def widget_observe(self, fn, names):
        self.get_widget().observe(fn, names=names)

    def update_ui(self, uindex):
        raise Exception('Do not call update_ui on base class')

    def update_data(self, uindex):
        raise Exception('Do not call update_data on an input-only class')

    def contains_widget(self, widget):
        return self.get_widget() == widget

    def list_innotations_tree(self):
        return [self]


class ImageInnotation(Innotation, DataMixin):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.path = kwargs.get('path', '')

        self.transform = kwargs.get('transform', None)

        self.annotation_styles = kwargs.get('annotation_styles', {})

        self.colorspace = 'BGR'
        if 'colorspace' in kwargs:
            self.colorspace = kwargs['colorspace']
            if self.colorspace not in ('BGR', 'RGB'):
                raise Exception("Parameter colorspace must be either 'RGB' or 'BGR'")

        self.max_repeats = 0

        self.watchlist = WatchList()

    def _create_widget(self):
        return ImagePad(wantwidth=self.width, wantheight=self.height, layout=self.layout, disabled=self.disabled,
                        annotation_styles=self.annotation_styles)

    def update_ui(self, uindex):
        if self.transform is None:
            it = self._get_data(uindex)
        else:
            it = self.transform(self._get_data(uindex))

        if hasattr(self._get_data(uindex), '__fspath__') or isinstance(self._get_data(uindex), str):
            # Path-like
            p = Path(it)
            if self.path != '':
                p = Path(self.path) / p
            self.get_widget().set_value_from_file(p)
        elif 'numpy' in str(type(it)) or 'Tensor' in str(type(it)):
            npim = it.numpy() if hasattr(it, 'numpy') else it
            if len(npim.shape) == 3 and npim.shape[2] not in (1,3,4):
                # Channels dim needs to be moved to back
                npim = npim.transpose((1,2,0))
            if not np.issubdtype(npim.dtype, np.integer):
                # Float so scale
                npim = (npim * 255).astype('int')

            if usecv2 and self.colorspace == 'RGB':
                npim = cv2.cvtColor(npim, cv2.COLOR_RGB2BGR)
            elif not usecv2 and self.colorspace == 'BGR' and len(npim.shape) == 3:
                npim = np.flip(npim, axis=2)

            if usecv2:
                self.get_widget().value = cv2.imencode('.png', npim)[1].tostring()
            else:
                pngbytes = io.BytesIO()
                pngmode = 'L' # Greyscale
                if len(npim.shape) == 3:
                    if npim.shape[2] > 4:
                        raise Exception("Image numpy array appears to have more than 4 channels")
                    pngmode = ('L','LA','RGB','RGBA')[npim.shape[2]-1]
                else:
                    npim = np.expand_dims(npim, axis=-1) # Need a third axis for channel
                pngim = png.from_array(npim, mode=pngmode) # Don't have BGR available so flipped to RGB above
                pngim.write(pngbytes) if hasattr(pngim, 'write') else pngim.save(pngbytes) # PyPNG API due to change after v0.0.19
                self.get_widget().value = pngbytes.getvalue()
                pngbytes.close()

        else:
            # Actual raw image data
            self.get_widget().value = it

    def setRect(self, name, repeat_index, x,y,w,h):
        watcher_index = self.watchlist.get_watcher_index(name, repeat_index)
        if watcher_index >= 0:
            self.get_widget().setRect(watcher_index, x,y,w,h)

    def register_bbox_watcher(self, name, repeat_index):
        self.max_repeats += 1
        self.get_widget().set_max_repeats(self.max_repeats)
        self.watchlist.add(Watcher(name=name, repeat_index=repeat_index))

    def get_current_watcher(self):
        return self.watchlist[self.get_widget().rect_index]

    def set_current_watcher(self, name, repeat_index):
        self.get_widget().rect_index = self.watchlist.get_watcher_index(name, repeat_index)

    def get_rect_for_watcher(self, name, repeat_index):
        watcher_index = self.watchlist.get_watcher_index(name, repeat_index)
        return self.get_widget().rects[watcher_index*4:(watcher_index+1)*4]


class BoundingBoxInnotation(Innotation, DataMixin):

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
            self.sourcedw.register_bbox_watcher(self.name, self.repeat_index)
            self.sourcedw.widget_observe(self.rectChanged, names='rects')
            self.sourcedw.widget_observe(self.rectIndexChanged, names='rect_index')
        self.get_widget().on_click(self.widget_clicked)

    def _create_widget(self):
        return FocusText(layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        self.get_widget().value = self._value_to_str(self._get_data(uindex))
        self._sync_to_image(uindex)

    def _sync_to_image(self, uindex):
        if self.sourcedw is not None:
            (x,y,w,h) = self._get_data(uindex)[:4]
            self.sourcedw.setRect(self.name, self.repeat_index, x,y,w,h)

    def _value_to_str(self, r):
        return ', '.join([str(int(a)) for a in r])

    def update_data(self, uindex):
        newval = self.get_widget().value
        if newval != self._value_to_str(self._get_data(uindex)):
            try:
                if self.repeat_index == -1:
                    self.data[uindex] = [int(float(s)) for s in re.split('[ ,]+', newval)]
                else:
                    self.data[uindex][self.repeat_index] = [int(float(s)) for s in re.split('[ ,]+', newval)]
                self._sync_to_image(uindex)
            except ValueError:
                pass

    def rectChanged(self, change):
        if self.sourcedw is not None:
            r = self.sourcedw.get_rect_for_watcher(self.name, self.repeat_index)
            #r = self.sourcedw.get_widget().rects
            #ri = self.repeat_index
            #if ri == -1:
            #    ri = 0
            #v = self._value_to_str(r[ri*4:ri*4+4])
            v = self._value_to_str(r)
            self.get_widget().value = v

    def rectIndexChanged(self, change):
        if self.sourcedw is not None:
            #if self.sourcedw.get_widget().rect_index == self.repeat_index:
            watcher = self.sourcedw.get_current_watcher()
            if watcher.name == self.name and watcher.repeat_index == self.repeat_index:
                self.get_widget().add_class('bounding-box-active')
            else:
                self.get_widget().remove_class('bounding-box-active')

    def widget_clicked(self, w):
        if self.sourcedw is not None:
            self.sourcedw.set_current_watcher(self.name, self.repeat_index)


class MultiClassInnotation(Innotation, DataMixin):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Just a 1-dim array with values corresponding to class numbers e.g. 0-5
        self.datadepth = 'simple'

        self.dims = 1
        if hasattr(self._get_data(0), '__len__'):
            self.dims = 2

        if self.dims > 1:
            if len(self._get_data(0)) == 1:
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
            m = len(self._get_data(0))-1
        elif self.datadepth == 'simple':
            m = max(self.data)  # TODO - use NumPy in case of repeat_index
        else: # colvector
            m = max(self.data)[0]  # TODO

        if m == 0:
            raise Exception(f'MultiClassInnotation {self.name} only has one class value in use so cannot infer class count - please specify a classes array')

        self.classes = [str(i) for i in range(m+1)]

    def _create_widget(self):
        if self.dropdown:
            return Dropdown(options=self.classes, layout=self.layout, disabled=self.disabled)
        return Select(options=self.classes, layout=self.layout, disabled=self.disabled)

    def _calc_class_index(self, uindex):
        if self.datadepth == 'onehot':
            return int(max(range(len(self._get_data(uindex))), key=lambda x: self._get_data(uindex)[x], default=0))
        if self.datadepth == 'simple':
            return int(self._get_data(uindex))
        # colvector
        return int(self._get_data(uindex)[0])

    def update_ui(self, uindex):
        self.get_widget().value = self.classes[self._calc_class_index(uindex)]

    def update_data(self, uindex):
        newval = self._get_widget_value()
        old_class_index = self._calc_class_index(uindex)
        if newval != self.classes[old_class_index]:
            class_index = self.classes.index(newval)
            if self.datadepth == 'onehot':
                self._set_data(uindex, old_class_index, 0)
                self._set_data(uindex, class_index, 1)
            elif self.datadepth == 'simple':
                self._set_data(uindex, class_index)
            else:
                # colvector
                self._set_data(uindex, 0, class_index)


class BinaryClassInnotation(MultiClassInnotation):

    def _guess_classes(self):
        self.classes = ['False', 'True']

    def _create_widget(self):
        return Checkbox(description=self.desc, layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        self.get_widget().value = bool(self._calc_class_index(uindex) == 1)

    def _get_widget_value(self):
        return self.classes[self.get_widget().value and 1 or 0]


class TextInnotation(Innotation, DataMixin):

    def __init__(self, *args, **kwargs):

        self.multiline = kwargs.get('multiline', True)

        super().__init__(*args, **kwargs)

    def _create_widget(self):
        if self.multiline:
            return Textarea(layout=self.layout, disabled=self.disabled)
        return Text(layout=self.layout, disabled=self.disabled)

    def update_ui(self, uindex):
        self.get_widget().value = str(self._get_data(uindex))

    def update_data(self, uindex):
        newval = str(self._get_widget_value())
        if newval != str(self._get_data(uindex)):
            self._set_data(uindex,  newval)
