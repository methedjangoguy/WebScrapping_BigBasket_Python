import json
import logging

from interface import FileSystemInterface
from workers.config_worker import RealFileSystem
import os

os.system("")

_config_logger = logging.getLogger("config")


class Config:
    def get_property(self, property):
        if property == "all":
            return self.config
        if property not in self.config.keys():
            return None
        return self.config[property]

    def run(self, fileSystem: FileSystemInterface, input: str):
        return fileSystem.read_file(input)
        pass

    def reload(self):
        self.config = json.loads(self.run(RFS, "./config/config.json"))
        _config_logger.info("Config reloaded")

    def __init__(self, filesystem):
        try:
            self.config = json.loads(self.run(filesystem, "./config/config.json"))
        except Exception as e:
            _config_logger.error(e)
        pass


RFS = RealFileSystem()
configuration = Config(RFS)
