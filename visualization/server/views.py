# -*- coding: utf-8 -*-
# @Author: ioriiod0
# @Date:   2017-07-12 13:24:54
# @Last Modified by:   ioriiod0
# @Last Modified time: 2017-07-13 23:57:12

import os
import time
from functools import wraps

from flask import request,redirect,session,g,Response,render_template
from itsdangerous import JSONWebSignatureSerializer as JWT
from flask_httpauth import HTTPTokenAuth
from schema import Schema, And, Use, Optional, SchemaError

from server import app
from server.errors import *
from server.logger import *
from server import models


logger = config_logger('SERVER.VIEWS', 'INFO', 'server.log')

# auth = HTTPTokenAuth('Bearer')

# ISFORMAT="%Y%m%d%H%M%S"

conn, cursor = models.init()

mydata = ""

@app.route("/api/v1", methods=["GET"])
def parse():
	global mydata
	req = request.args
	# .args.get('username')
	if "company" in req:
		company_code = req["company"]
		mydata = models.execute(conn, cursor, ("company", company_code))
	elif "person" in req:
		name = req["person"]
		mydata = models.execute(conn, cursor, ("person", name))		
	# return {"resultmsg":"OK","resultno":ERROR_OK},200
	return render_template('index.html')


@app.route("/api/data")
def data():
	return mydata

