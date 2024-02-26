from interface.FileSystemInterface import FileSystemInterface
import sqlite3


class RealFileSystem(FileSystemInterface):
    def read_file(self, filename):
        data = ""
        with open(filename, "r") as f:
            data = f.read()
        return data
