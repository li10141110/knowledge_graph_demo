# -*- coding: utf-8 -*-
# @Author: ioriiod0
# @Date:   2017-07-12 11:47:28
# @Last Modified by:   ioriiod0
# @Last Modified time: 2017-07-14 19:21:37

import gevent
from gevent.monkey import patch_all
patch_all()
from server import app
from server.config import *

if __name__ == '__main__':
    if LOCAL_TEST:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=8080)
