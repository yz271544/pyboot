#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: Switch.py
@author: lyndon
@time: Created on 2021-02-01 16:11
@env: Python
@desc:
@ref:
@blog:
"""

REHEARSAL_START_STATUS = 6
REHEARSAL_SUCCESS_STATUS = 7
REHEARSAL_ERROR_STATUS = 13


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

    def get(self):
        pass


class RehearsalStatusSwitch(Switch):
    def __init__(self, v):
        super().__init__(v)

    def get(self):
        for case in self:
            if case("start"):
                return REHEARSAL_START_STATUS
            if case("success"):
                return REHEARSAL_SUCCESS_STATUS
            if case("error"):
                return REHEARSAL_ERROR_STATUS
            if case():
                print("unknown rehearsal!")


if __name__ == '__main__':

    v = 'ten'
    for case in Switch(v):
        if case("one"):
            print(1)
            break
        if case('two'):
            print(2)
            break
        if case('ten'):
            print(10)
            break
        if case('eleven'):
            print(11)
            break
        if case():  # default, could also just omit condition or 'if True'
            print("something else!")
            # No need to break here, it'll stop anyway

    print("=================================================================")


    v = "start"

    startRehearsalStatusSwitch = RehearsalStatusSwitch(v).get()
    print(startRehearsalStatusSwitch)

    print(RehearsalStatusSwitch("success").get())
    print(RehearsalStatusSwitch("error").get())

    print(RehearsalStatusSwitch("success"))
