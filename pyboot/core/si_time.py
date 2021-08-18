#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@author: lyndon
@time Created on 2019/2/13 15:59
@desc
"""
import datetime


class SiTime:

    @staticmethod
    def curdate():
        return datetime.datetime.now().strftime('%Y%m%d')

    @staticmethod
    def curtime():
        return datetime.datetime.now().strftime('%H%M%S')

    @staticmethod
    def showCurTime():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def showTime():
        return "[%s]" % datetime.datetime.now().strftime('%H:%M:%S')

    @staticmethod
    def today():
        return datetime.date.today()

    @classmethod
    def yesdate(cls):
        return cls.today() - datetime.timedelta(days=1)

    @classmethod
    def two_mon_today(cls):
        return cls.today() - datetime.timedelta(days=62)


if __name__ == '__main__':
    print(SiTime.curdate())
    print(SiTime.curtime())
    print(SiTime.showCurTime())
    print(SiTime.showTime())
    print(SiTime.today())
    print(SiTime.yesdate())
    print(SiTime.yesdate().strftime('%Y%m%d'))
    print(type(SiTime.yesdate()))
    print(SiTime.two_mon_today())


