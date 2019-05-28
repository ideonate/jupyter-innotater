from collections import namedtuple

Watcher = namedtuple('Watcher', 'name repeat_index')


class WatchList:

    def __init__(self):
        self.wl = []

    def add(self, watcher):
        self.wl.append(watcher)

    def __getitem__(self, item):
        return self.wl[item]

    def __len__(self):
        return len(self.wl)

    def get_watcher_index(self, name, repeat_index):
        for i in range(len(self.wl)):
            if self.wl[i].name == name and self.wl[i].repeat_index == repeat_index:
                return i
        return -1
