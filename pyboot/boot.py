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
from conf import BaseConfig
from pyboot.logger import log
from pyboot.starter import GetStarters
from starter_context import StarterContext


# 应用程序
class BootApplication:
	IsTest: bool
	conf: BaseConfig
	starterCtx: StarterContext

	# 构造系统
	def __init__(self, IsTest: bool, conf: BaseConfig, starterCtx: StarterContext):
		self.IsTest = IsTest
		self.conf = conf
		self.starterCtx = starterCtx

	# 程序初始化
	def init(self):
		log.info("Initializing starters...")
		for starter in GetStarters():
			log.Debugf("Initializing: PriorityGroup=%d,Priority=%d", self.PriorityGroup(), self.Priority())
			starter.Init(self.starterCtx)

	# 程序安装
	def setup(self):
		log.Info("Setup starters...")
		for starter in GetStarters():
			starter.Setup(self.starterCtx)

	# 程序开始运行，开始接受调用
	def start(self):
		log.Info("Starting starters...")
		for starter in GetStarters():
			if self.starterCtx.Props().get("testing"):
				starter.Start(self.starterCtx)
				continue
			if starter.StartBlocking() is False:
				starter.Start(self.starterCtx)
		for starter in GetStarters():
			if starter.StartBlocking():
				starter.Start(self.starterCtx)

	# 程序开始运行，开始接受调用
	def Stop(self):
		log.Info("Stoping starters...")
		for starter in GetStarters():
			starter.Stop(self.starterCtx)

	def Start(self):
		# 1.初始化starter
		self.init()
		# 2. 安装starter
		self.setup()
		# 3. 启动starter
		self.start()
