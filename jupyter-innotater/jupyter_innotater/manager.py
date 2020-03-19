from .data import Innotation
from .mixins import DataMixin


class DataManager:

    def __init__(self, inputs, targets, indexes=None):

        if inputs is None: inputs = []
        if targets is None: targets = []

        self.inputs = [inputs] if isinstance(inputs, Innotation) else inputs
        self.targets = [targets] if isinstance(targets, Innotation) else targets

        self.alldws = {}

        l = -1

        for dw in self.inputs+self.targets:
            l = self._add_to_alldws(dw, l)

        self.underlying_len = l

        self.indexes = indexes
        if indexes is not None:
            if len(indexes) == 0:
                raise Exception("indexes must be a non-empty array-like containing integers or booleans")

            # boolean or numpy.bool_ - and might be a col vector
            if 'bool' in str(type(indexes[0])) or hasattr(indexes[0], '__len__') and len(indexes[0]) == 1 and 'bool' in str(type(indexes[0][0])):
                if len(indexes) != len(self.inputs[0]):
                    raise Exception("indexes as a boolean mask must have same len as the inputs")
                self.indexes = [int(i) for i in range(len(indexes)) if hasattr(indexes[i], '__len__') and indexes[i][0] or indexes[i] == True]
                if len(self.indexes) == 0:
                    raise Exception("indexes as a boolean mask must have some True values")

        for dw in list(self.alldws.values()):
            dw.post_register(self)

    def _add_to_alldws(self, dw, l):
        for onedw in dw.list_innotations_tree():
            name = onedw.name
            if name in self.alldws:
                raise Exception(f'Duplicate Innotation {name}')

            self.alldws[name] = onedw

        # Check number of rows is the same and not zero
        if isinstance(dw, DataMixin):
            this_len = len(dw)
            if l == -1:
                if this_len == 0:
                    raise Exception(f'Innotation {type(dw)} {name} has 0 data rows')
                l = this_len
            elif l != this_len:
                raise Exception(f'Innotations must all have same number of rows: {type(dw)} {name} has a different number of data rows than previous Innotations')

        return l

    def get_data_wrapper_by_name(self, name):
        if name in self.alldws:
            return self.alldws[name]
        return None

    def get_data_wrappers_by_type(self, klass):
        return [dw for dw in self.alldws.values() if isinstance(dw, klass)]

    def get_data_len(self):
        if self.indexes is not None:
            return len(self.indexes)
        if len(self.inputs):
            return len(self.inputs[0])
        return len(self.targets[0])

    def get_underlying_index(self, index):
        if self.indexes is None:
            return index
        return self.indexes[index]

    def get_inputs(self):
        return self.inputs

    def get_targets(self):
        return self.targets

    def get_all(self):
        return self.alldws.values()

    def is_input(self, dw):
        return dw in self.inputs

    def dynamic_add_innotations(self, inputs, targets):
        self.inputs.extend(inputs)
        self.targets.extend(targets)

        for dw in inputs+targets:
            self._add_to_alldws(dw, self.underlying_len)

        for dw in inputs+targets:
            dw.post_register(self)
