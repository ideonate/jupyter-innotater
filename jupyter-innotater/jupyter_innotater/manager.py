from .data import Innotation
from .mixins import DataMixin


class DataManager:

    def __init__(self, inputs, targets, indexes=None):
        """
        Initialize the inputs.

        Args:
            self: (todo): write your description
            inputs: (list): write your description
            targets: (todo): write your description
            indexes: (str): write your description
        """

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
        """
        Convert a dw object to a dw object.

        Args:
            self: (todo): write your description
            dw: (todo): write your description
            l: (todo): write your description
        """
        for onedw in dw.list_innotations_tree():
            name = onedw.name
            if name in self.alldws:
                raise Exception('Duplicate Innotation {}'.format(name))

            self.alldws[name] = onedw

        # Check number of rows is the same and not zero
        if isinstance(dw, DataMixin):
            this_len = len(dw)
            if l == -1:
                if this_len == 0:
                    raise Exception('Innotation {} {} has 0 data rows'.format(type(dw), name))
                l = this_len
            elif l != this_len:
                raise Exception('Innotations must all have same number of rows: {} {} has a different number of data rows than previous Innotations'.format(type(dw), name))

        return l

    def get_data_wrapper_by_name(self, name):
        """
        Return the data type by name.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        if name in self.alldws:
            return self.alldws[name]
        return None

    def get_data_wrappers_by_type(self, klass):
        """
        Get the klass of the given klass.

        Args:
            self: (todo): write your description
            klass: (todo): write your description
        """
        return [dw for dw in self.alldws.values() if isinstance(dw, klass)]

    def get_data_len(self):
        """
        Returns the length of the data array.

        Args:
            self: (todo): write your description
        """
        if self.indexes is not None:
            return len(self.indexes)
        if len(self.inputs):
            return len(self.inputs[0])
        return len(self.targets[0])

    def get_underlying_index(self, index):
        """
        Return the index of the given index.

        Args:
            self: (todo): write your description
            index: (int): write your description
        """
        if self.indexes is None:
            return index
        return self.indexes[index]

    def get_inputs(self):
        """
        Returns a list of inputs.

        Args:
            self: (todo): write your description
        """
        return self.inputs

    def get_targets(self):
        """
        Returns a list of targets.

        Args:
            self: (todo): write your description
        """
        return self.targets

    def get_all(self):
        """
        Returns all the values

        Args:
            self: (str): write your description
        """
        return self.alldws.values()

    def is_input(self, dw):
        """
        Returns true if input is_input_input.

        Args:
            self: (todo): write your description
            dw: (int): write your description
        """
        return dw in self.inputs

    def dynamic_add_innotations(self, inputs, targets):
        """
        Add the dynamic input targets.

        Args:
            self: (todo): write your description
            inputs: (todo): write your description
            targets: (list): write your description
        """
        self.inputs.extend(inputs)
        self.targets.extend(targets)

        for dw in inputs+targets:
            self._add_to_alldws(dw, self.underlying_len)

        for dw in inputs+targets:
            dw.post_register(self)
