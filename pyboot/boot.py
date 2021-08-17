#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: boot.py
@author: etl
@time: Created on 8/13/21 9:36 AM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.conf import BaseConfig
from pyboot.logger import log
# from pyboot.starter import GetStarters
from pyboot.starter import StarterRegister
from starter_context import StarterContext


# 应用程序
class BootApplication:
	# IsTest: bool
	# conf: BaseConfig
	# starterCtx: StarterContext

	# 构造系统
	def __init__(self, IsTest: bool, starterCtx: StarterContext, starterRegister: StarterRegister):
		self.IsTest = IsTest
		self.starterCtx = starterCtx
		self.startRegister = starterRegister

	# 程序初始化
	def init(self):
		log.info("Initializing starters...")
		starters = self.startRegister.AllStarters()
		for starter in starters:
			log.debug("Initializing: PriorityGroup=%d,Priority=%d", starter.PriorityGroup(), starter.Priority())
			starter.Init(self.starterCtx)

	# 程序安装
	def setup(self):
		log.info("Setup starters...")
		for starter in self.startRegister.AllStarters():
			starter.Setup(self.starterCtx)

	# 程序开始运行，开始接受调用
	def start(self):
		log.info("Starting starters...")
		for starter in self.startRegister.AllStarters():
			if starter.StartBlocking() is False:
				starter.Start(self.starterCtx)
		for starter in self.startRegister.AllStarters():
			if starter.StartBlocking():
				starter.Start(self.starterCtx)

	# 程序开始运行，开始接受调用
	def Stop(self):
		log.Info("Stoping starters...")
		for starter in self.startRegister.AllStarters():
			starter.Stop(self.starterCtx)

	def Start(self):
		# 1.初始化starter
		self.init()
		# 2. 安装starter
		self.setup()
		# 3. 启动starter
		self.start()
