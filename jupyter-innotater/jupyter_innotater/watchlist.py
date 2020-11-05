from collections import namedtuple

Watcher = namedtuple('Watcher', 'name repeat_index')


class WatchList:

    def __init__(self):
        """
        Initialize the data

        Args:
            self: (todo): write your description
        """
        self.wl = []

    def add(self, watcher):
        """
        Add a watcher.

        Args:
            self: (todo): write your description
            watcher: (todo): write your description
        """
        self.wl.append(watcher)

    def __getitem__(self, item):
        """
        Return the item from item

        Args:
            self: (todo): write your description
            item: (str): write your description
        """
        return self.wl[item]

    def __len__(self):
        """
        Returns the length of the record.

        Args:
            self: (todo): write your description
        """
        return len(self.wl)

    def get_watcher_index(self, name, repeat_index):
        """
        Return the index of a watcher.

        Args:
            self: (todo): write your description
            name: (str): write your description
            repeat_index: (int): write your description
        """
        for i in range(len(self.wl)):
            if self.wl[i].name == name and self.wl[i].repeat_index == repeat_index:
                return i
        return -1
