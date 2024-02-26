from abc import abstractmethod


class FileSystemInterface:
    @abstractmethod
    def read_file(self, filename):
        pass

    def __init__(self):
        pass
