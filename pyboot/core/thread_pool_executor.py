#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: thread_pool_executor.py
@author: lyndon
@time: Created on 2021-01-21 12:37
@env: Python
@desc:
@ref:
@blog:
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pyboot.core.si_time import SiTime
from pyboot.logger import log


class Step:
    def __init__(self, sid, name, func, params):
        self.sid = sid
        self.name = name
        self.func = func
        self.params = params
        self.status = 0
        self.remark = ""

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_result(self):
        return self.status, self.remark

    def run_step(self):
        try:
            print(SiTime.showCurTime() + " " + threading.currentThread().getName() + " run body step sid:" + str(
                self.sid) + " name:" + self.name)
            funcRet = self.func(*self.params)
            # time.sleep(0.5)
            log.info("funcRet:" + str(funcRet))
            self.status = 0
        except Exception as e:
            print(e)
            self.status = -1
            self.remark = str(e)
            raise e


class Task:
    def __init__(self, tid, name):
        self.tid = tid
        self.name = name
        self.steps = []
        self.callback = None
        self.status = 0
        self.remark = ""

    def get_name(self):
        return self.name

    def get_steps(self):
        return self.steps

    def add_steps(self, *steps: Step):
        for sp in steps:
            self.steps.append(sp)

    def run_steps(self):
        start = time.time()
        for step in self.steps:
            try:
                step.run_step()
            except Exception as e:
                log.error(e)
                self.status, self.remark = step.get_result()
                break
        end = time.time()
        print("Running time: %s seconds" % (end - start))
        # return self.status # Fuck！仅仅返回status是不够的，即便是用lambda方式也无法传输task.name
        return {"tid": self.tid, "name": self.name, "status": self.status, "remark": self.remark}

    def set_callback(self, callback):
        self.callback = callback

    def get_callback(self):
        return self.callback


class MyTask(Task):
    def __init__(self, tid, name):
        super().__init__(tid, name)


class TaskExecutor:

    def __init__(self, name, prefix):
        self.name = name
        self.tpool = ThreadPoolExecutor(max_workers=5, thread_name_prefix=prefix)

    def submit(self, task: Task):
        self.tpool.submit(task.run_steps).add_done_callback(task.get_callback())


class CallBack:
    def __init__(self, callback):
        self.callback = callback

    def callback(self):
        return self.callback

    def __call__(self, *args, **kwargs):
        self.callback(*args, **kwargs)


if __name__ == '__main__':
    ter = TaskExecutor("test", "sub-test-task")


    def run(context):
        print("run print:" + context)


    def write_meta(res):
        print("write meta stop this task!" + str(res.result()))


    ts1 = Step(sid=1001, name="step1001", func=run, params=["body of step1001"])
    ts2 = Step(sid=1002, name="step1002", func=run, params=["body of step1002"])
    ts3 = Step(sid=1003, name="step1003", func=run, params=["body of step1003"])

    task1 = MyTask(tid=100, name="task1")
    task1.add_steps(ts1, ts2, ts3)

    callBack1 = CallBack(write_meta)
    # callBack = write_meta
    task1.set_callback(callBack1)

    ter.submit(task1)

    ts21 = Step(sid=2001, name="step2001", func=run, params=["body of step2001"])
    ts22 = Step(sid=2002, name="step2002", func=run, params=["body of step2002"])
    ts23 = Step(sid=2003, name="step2003", func=run, params=["body of step2003"])

    task2 = MyTask(tid=101, name="task2")
    task2.add_steps(ts21, ts22, ts23)

    callBack = CallBack(write_meta)
    task2.set_callback(callBack)

    ter.submit(task2)
