from .data import DataWrapper

class DataManager:

    def __init__(self, inputs, targets):

        self.inputs = [inputs] if isinstance(inputs, DataWrapper) else inputs
        self.targets = [targets] if isinstance(targets, DataWrapper) else targets

        self.alldws = {}

        for dw in self.inputs+self.targets:
            name = dw.get_name()
            if name in self.alldws:
                raise Exception(f'Duplicate DataWrapper {name}')

            self.alldws[name] = dw

        for dw in self.alldws.values():
            dw.post_register(self)

    def get_data_wrapper_by_name(self, name):
        if name in self.alldws:
            return self.alldws[name]
        return None

    def get_data_wrappers_by_type(self, klass):
        return [dw for dw in self.alldws.values() if isinstance(dw, klass)]

    def get_data_len(self):
        return len(self.inputs[0])

    def get_inputs(self):
        return self.inputs

    def get_targets(self):
        return self.targets

    def get_all(self):
        return self.alldws.values()
