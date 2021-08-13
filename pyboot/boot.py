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
from starter_context import StarterContext


# 应用程序
class BootApplication:
	IsTest: bool
	# conf: kvs.ConfigSource
	starterCtx: StarterContext

	# def __init__(self):

#
# # 构造系统
# def New(conf kvs.ConfigSource) *BootApplication {
# 	e := &BootApplication{conf: conf, starterCtx: StarterContext{}}
# 	e.starterCtx.SetProps(conf)
# 	return e
# }
#
# func (b *BootApplication) Start() {
# 	//1. 初始化starter
# 	b.init()
# 	//2. 安装starter
# 	b.setup()
# 	//3. 启动starter
# 	b.start()
# }
#
# //程序初始化
# func (e *BootApplication) init() {
# 	log.Info("Initializing starters...")
# 	for _, v := range GetStarters() {
# 		typ := reflect.TypeOf(v)
# 		log.Debugf("Initializing: PriorityGroup=%d,Priority=%d,type=%s", v.PriorityGroup(), v.Priority(), typ.String())
# 		v.Init(e.starterCtx)
# 	}
# }
#
# //程序安装
# func (e *BootApplication) setup() {
#
# 	log.Info("Setup starters...")
# 	for _, v := range GetStarters() {
# 		typ := reflect.TypeOf(v)
# 		log.Debug("Setup: ", typ.String())
# 		v.Setup(e.starterCtx)
# 	}
#
# }
#
# //程序开始运行，开始接受调用
# func (e *BootApplication) start() {
#
# 	log.Info("Starting starters...")
# 	for i, v := range GetStarters() {
#
# 		typ := reflect.TypeOf(v)
# 		log.Debug("Starting: ", typ.String())
# 		if e.starterCtx.Props().GetBoolDefault("testing", false) {
# 			go v.Start(e.starterCtx)
# 			continue
# 		}
#
# 		if v.StartBlocking() {
# 			if i+1 == len(GetStarters()) {
# 				v.Start(e.starterCtx)
# 			} else {
# 				go v.Start(e.starterCtx)
# 			}
# 		} else {
# 			v.Start(e.starterCtx)
# 		}
#
# 	}
# }
#
# //程序开始运行，开始接受调用
# func (e *BootApplication) Stop() {
#
# 	log.Info("Stoping starters...")
# 	for _, v := range GetStarters() {
# 		typ := reflect.TypeOf(v)
# 		log.Debug("Stoping: ", typ.String())
# 		v.Stop(e.starterCtx)
# 	}
# }
