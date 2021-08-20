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
from pyboot.logger import log
from pyboot.starter import GetStarters
from starter_context import StarterContext


# 应用程序
class BootApplication:

	# 构造系统
	def __init__(self, IsTest: bool, starterCtx: StarterContext):
		self.IsTest = IsTest
		self.starterCtx = starterCtx

	# 程序初始化
	def init(self):
		log.info("Initializing starters...")
		starters = GetStarters()
		log.debug("starter len:%d", len(starters))
		for starter in starters:
			log.debug("Initializing: PriorityGroup=%d,Priority=%d", starter.PriorityGroup(), starter.Priority())
			starter.Init(self.starterCtx)

	# 程序安装
	def setup(self):
		log.info("Setup starters...")
		starters = GetStarters()
		for starter in starters:
			starter.Setup(self.starterCtx)

	# 程序开始运行，开始接受调用
	def start(self):
		log.info("Starting starters...")
		starters = GetStarters()
		for starter in starters:
			if starter.StartBlocking() is False:
				starter.Start(self.starterCtx)
		starters = GetStarters()
		for starter in starters:
			if starter.StartBlocking():
				starter.Start(self.starterCtx)

	# 程序开始运行，开始接受调用
	def Stop(self):
		log.Info("Stoping starters...")
		starters = GetStarters()
		for starter in starters:
			starter.Stop(self.starterCtx)

	def Start(self):
		# 1.初始化starter
		self.init()
		# 2. 安装starter
		self.setup()
		# 3. 启动starter
		self.start()
