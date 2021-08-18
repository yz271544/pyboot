#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: ExecutorServer.py
@author: lyndon
@time: Created on 2021-01-22 10:50
@env: Python
@desc:
@ref:
@blog:
"""
import threading

from pyboot.conf.settings import PROFILE
from pyboot.core.Generator import Generator
from pyboot.core.thread_pool_executor import TaskExecutor, Task, Step, CallBack
from pyboot.logger import log
from pyboot.utils.common.SnowflakeId import IdWorker
from pyboot.core.Switch import RehearsalStatusSwitch


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class ExecutorServer:

    def __init__(self):
        self.generator = Generator()
        self.ter = TaskExecutor("task-executor", "sub-datacenter-task")
        self.id_worker = IdWorker()

        self.running_tasks = []
        self.R = threading.Lock()

    def responseOK(self, cid):
        return "{cid} start rehearsal".format(cid=cid)

    def callBackUpdateCustmGrpStatus(self, res):
        result = res.result()
        cid = result["name"]
        print("callBackUpdateCustmGrpStatus res:", result)

        rehearsal_status = RehearsalStatusSwitch("success").get() if result["status"] == 0 else RehearsalStatusSwitch(
            "error").get()

        self.R.acquire()
        if PROFILE == "dev":
            self.custmGrpBasInfoService.updateStatusById(cid, rehearsal_status)
            print("self.custmGrpBasInfoService.updateStatusById({}, {})".format(result["name"], rehearsal_status))
            log.info("self.custmGrpBasInfoService.updateStatusById({}, {})".format(result["name"], rehearsal_status))
        else:
            self.custmGrpBasInfoService.updateStatusById(cid, rehearsal_status)
            print("self.custmGrpBasInfoService.updateStatusById({}, {})".format(result["name"], rehearsal_status))
            log.info("self.custmGrpBasInfoService.updateStatusById({}, {})".format(result["name"], rehearsal_status))
        self.running_tasks.remove(cid)
        self.R.release()
        return 0

    def run_by_id(self, id):
        self.R.acquire()
        existsNotToRun = len(list({id}.intersection(set(self.running_tasks)))) > 0
        if existsNotToRun:
            self.R.release()
            return "{} was is already running!".format(id)
        else:
            self.running_tasks.append(id)
            self.R.release()
            generate_tasks = self.generator.generate_by_id(id)
            self.run(generate_tasks)
            return "running {}".format(id)

    def run_by_state(self, status):
        custmGrpBasInfoList = self.custmGrpBasInfoService.getByStatus(status)
        want_to_run_ids = [custmGrpBasInfo.id for custmGrpBasInfo in custmGrpBasInfoList if
                           custmGrpBasInfo.custm_grp_stat == 0]
        dispatch_ids = list(set(want_to_run_ids).difference(self.running_tasks))
        for cid in dispatch_ids:
            self.run_by_id(cid)

    def run(self, generate_tasks):
        # generate_tasks = self.generator.generate_by_status(0)
        for task_text in generate_tasks:
            cleanStep = Step(sid=self.id_worker.get_id(), name="clean", func=self.datacenter.execsql,
                             params=[task_text["clean"]])
            createStep = Step(sid=self.id_worker.get_id(), name="create", func=self.datacenter.execsql,
                              params=[task_text["create"]])
            insertStep = Step(sid=self.id_worker.get_id(), name="insert", func=self.datacenter.execsql,
                              params=[task_text["insert"]])

            analysis_create_step = Step(sid=self.id_worker.get_id(), name="analysis_create",
                                        func=self.datacenter.execsql, params=[task_text["analysis_create"]])
            delete_partition_step = Step(sid=self.id_worker.get_id(), name="delete_partition",
                                         func=self.datacenter.execsql,
                                         params=[task_text["delete_partition"]])

            create_partition_step = Step(sid=self.id_worker.get_id(), name="create_partition",
                                         func=self.datacenter.execsql,
                                         params=[task_text["create_partition"]])

            analysis_insert_step = Step(sid=self.id_worker.get_id(), name="analysis_insert",
                                        func=self.datacenter.execsql,
                                        params=[task_text["analysis_insert"]])

            task = Task(tid=self.id_worker.get_id(), name=task_text["taskid"])

            task.add_steps(cleanStep, createStep, insertStep, analysis_create_step, delete_partition_step,
                           create_partition_step, analysis_insert_step)

            # Fuck！ 如果用lambda方式，传输task.get_name()，其实callBackUpdateCustmGrpStatus函数只能收到最后一个任务的name
            # 所以，将thread_pool_executor中的Task.run_steps方法的返回值改为了返回一个dict，
            # 则callBackUpdateCustmGrpStatus函数通过res.result()函数获取这个dict的内容
            # callback = CallBack(
            #     lambda x: self.callBackUpdateCustmGrpStatus(task.get_name(), 1) if x.result() == 0 else -1)
            # task.set_callback(callback)

            callback = CallBack(self.callBackUpdateCustmGrpStatus)
            task.set_callback(callback)
            self.ter.submit(task)
