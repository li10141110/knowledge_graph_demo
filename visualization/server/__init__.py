# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2017-08-30 16:53:31 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2017-08-30 16:53:31 


from flask import Flask

app = Flask("KG_API")
app.config.from_object("server.config")

import views
import models
