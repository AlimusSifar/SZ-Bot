from os import path, mkdir
import logging


class Config(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def mkdir_if_not_exists(pathname):
    if not path.exists(pathname):
        mkdir(pathname)


configs = Config()
configs.level = logging.INFO
configs.filename = 'log/logs.log'
# configs.encoding = 'utf-8'
configs.filemode = 'w'
configs.format = ('[%(levelname)s] at [%(asctime)s] from [%(name)s] inside [%(funcName)s] function '
                  'on [line %(lineno)s]:\n%(message)s')
mkdir_if_not_exists('log')
logging.basicConfig(**configs)
