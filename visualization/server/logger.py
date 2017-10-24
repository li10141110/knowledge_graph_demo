# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-30 16:54:38 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-30 16:54:38 


import logging
import logging.handlers

def config_logger(name, level, f = None):
     LEVEL = getattr(logging, level.upper(), None)
     logger = logging.getLogger(name)
     logger.propagate = False #don't propagate to root logger!
     logger.setLevel(LEVEL)
     formatter = logging.Formatter('%(asctime)s - %(process)d - %(thread)d - %(name)s - %(levelname)s - %(message)s')
     if f:
          fh = logging.handlers.RotatingFileHandler(f, maxBytes=1024*1024*50, backupCount=5)
          fh.setLevel(LEVEL)
          fh.setFormatter(formatter)
          logger.addHandler(fh)
     else:
          sh = logging.StreamHandler()
          sh.setLevel(LEVEL)
          sh.setFormatter(formatter)
          logger.addHandler(sh)
     return logger
