#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: flask_server.py
@author: etl
@time: Created on 8/19/21 1:55 PM
@env: Python @desc:
@ref: @blog:
"""
import time
import sys
from pyboot import web
from flask import Flask, request
from pyboot.web.flask import routes
from pyboot.conf.settings import SERV_PORT
from pyboot.logger import log
from pyboot.web import WebApp
from pyboot.starter import BaseStarter


class FlaskStarter(BaseStarter):
    def Init(self, starter_context):
        log.info("FlaskStarter Init start")
        self.initWebApp()
        log.info("FlaskStarter Init end")
        return

    def Setup(self, starter_context):
        log.info("FlaskStarter Setup start")
        routes.init_app(web.webApp)
        log.info("FlaskStarter Setup end")
        return

    def Start(self, starter_context):
        log.info("FlaskStarter Start start")
        app = WebApp()
        app.run(host='0.0.0.0', port=SERV_PORT, debug=False, threaded=False)
        log.info("FlaskStarter Start end")
        return

    def Stop(self, starter_context):
        log.info("FlaskStarter Stop start")
        self.stop_server()
        log.info("FlaskStarter Stop end")
        return

    def StartBlocking(self) -> bool:
        return True

    def initWebApp(self):
        web.webApp = Flask(__name__)
        web.webApp.config.from_object('pyboot.conf.settings')

    def stop_server(self, *args, **kwargs):
        # stop_serv_func = request.environ.get('werkzeug.server.shutdown')
        # if stop_serv_func is None:
        #     raise RuntimeError('Not running with the Werkzeug Server')
        # stop_serv_func()
        sys.exit(0)
