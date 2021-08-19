#!/usr/bin/env python
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: tornado_server.py
@author: etl
@time: Created on 8/17/21 2:23 PM
@env: Python @desc:
@ref: @blog:
"""
import time
import sys
from pyboot import web
from pyboot.logger import log
from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext
from pyboot.web import WebApp
import tornado.web
import tornado.ioloop
import tornado.httpserver

from pyboot.web.tornado.EdgeSubProcessQueue import EdgeSubProcessQueue
from pyboot.web.tornado.TornadoRoute import IndexHandler
from pyboot.conf.settings import SERV_PORT

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3


class TornadoServer(BaseStarter):

    httpServer = None

    def Init(self, starter_context: StarterContext):
        log.info("TornadoServer Init start")
        log.info("TornadoServer Init end")
        routes = self.buildRoute()
        self.initWebApp(routes)
        return

    def Setup(self, starter_context: StarterContext):
        return

    def Start(self, starter_context: StarterContext):
        app = WebApp()
        global httpServer
        httpServer = tornado.httpserver.HTTPServer(app, xheaders=True)
        httpServer.listen(SERV_PORT)

        tornado.ioloop.IOLoop.instance().start()
        log.info("Exit...")
        return

    def Stop(self, starter_context: StarterContext):
        print("tornado Stop begin")
        self.sig_handler()
        print("tornado Stop end")
        sys.exit(0)

    def StartBlocking(self) -> bool:
        return True

    def initWebApp(self, routes):
        web.webApp = tornado.web.Application(routes)

    def buildRoute(self):
        routes = []
        routes = routes + [
            (r'/', IndexHandler),
            (r'/queue_size_metrics', EdgeSubProcessQueue),
        ]
        return routes

    def sig_handler(self):
        tornado.ioloop.IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        log.info("Stopping HttpServer...")
        httpServer.stop()

        log.info("IOLoop Will be Terminate in %s Seconds...", MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        instance = tornado.ioloop.IOLoop.instance()
        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def terminate():
            now = time.time()
            # if now < deadline and (instance._callbacks or instance._timeouts):
            if now < deadline:
                    instance.add_timeout(now + 1, terminate)
            else:
                instance.stop()
                log.info("Shutdown...")
            instance.stop()
            log.info("ShutDown")
        terminate()

