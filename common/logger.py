#coding=utf-8
import logging.config
import os
import yaml

os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

class Logger():

    def __init__(self,logger=None):
        self.logger=logging.getLogger(logger)
        default_level=logging.INFO
        dirname = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = dirname + '\config\logging.yaml'
        if os.path.exists(path):
            with open(path,'rt',encoding="utf-8") as f:
                config=yaml.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
            print("该yaml日志配置文件不存在,请检查路径")

    def getLogger(self):
        return self.logger


