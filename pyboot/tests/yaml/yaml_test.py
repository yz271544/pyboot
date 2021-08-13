#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: yaml_test.py
@author: etl
@time: Created on 8/13/21 9:38 AM
@env: Python @desc:
@ref: @blog:
"""

import unittest
import yaml
import os
import re

os.path.join(os.getcwd())


class Monster(yaml.YAMLObject):
     yaml_tag = u'!Monster'
     def __init__(self, name, hp, ac, attacks):
         self.name = name
         self.hp = hp
         self.ac = ac
         self.attacks = attacks
     def __repr__(self):
         return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
             self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)

class Dice(tuple):
     def __new__(cls, a, b):
         return tuple.__new__(cls, [a, b])
     def __repr__(self):
         return "Dice(%s,%s)" % self


class Hero:
     def __init__(self, name, hp, sp):
         self.name = name
         self.hp = hp
         self.sp = sp

     def __repr__(self):
         return "%s(name=%r, hp=%r, sp=%r)" % (
             self.__class__.__name__, self.name, self.hp, self.sp)


class YamlTest(unittest.TestCase):

    def tearDown(self) -> None:
        yaml.warnings({'YAMLLoadWarning': False})

    def test_hello(self):
        print("------------------------- test_hello -------------------------------")
        t1 = yaml.load(u"""
        hello: Привет!
        """, Loader=yaml.FullLoader)
        print(t1)
        print(yaml.dump([1, 2, 3], explicit_start=True))
        print(yaml.dump_all([1, 2, 3], explicit_start=True))

    def test_read_file(self):
        print("------------------------ test_read_file --------------------------------")
        with open("/pyboot/tests/yaml/document.yaml", 'r') as stream:
            for data in yaml.load_all(stream, Loader=yaml.FullLoader):
                print(data)

    def test_read_from_file(self):

        print("--------------------------- test_read_from_file -----------------------------")
        conf = os.path.join(os.getcwd(), "document.yaml")
        df = open(conf, 'r')
        config = yaml.load_all(df.read(), Loader=yaml.FullLoader)
        for context in config:
            print(context)
        df.close()

    def test_dump(self):
        print(yaml.dump({'name': 'Silenthand Olleander', 'race': 'Human', 'traits': ['ONE_HAND', 'ONE_EYE']}))

    def test_dump_class(self):
        hero = Hero("Galain Ysseleg", hp=-3, sp=2)
        print(hero)
        print(yaml.dump(hero))

    # def test_constructor(self):
    #     m = yaml.load("""
    #     --- !Monster
    #     name: Cave spider
    #     hp: [2,6]    # 2d6
    #     ac: 16
    #     attacks: [BITE, HURT]
    #     """)
    #     print(m)

    def test_meta(self):
        print("--------------------------- test_meta -----------------------------")
        print(Dice(3, 6))
        print(yaml.dump(Dice(3, 6)))

        def dice_representer(dumper, data):
            return dumper.represent_scalar(u'!dice', u'%sd%s' % data)

        yaml.add_representer(Dice, dice_representer)
        print(yaml.dump({'gold': Dice(10, 6)}))

        def dice_constructor(loader, node):
            value = loader.construct_scalar(node)
            a, b = map(int, value.split('d'))
            return Dice(a, b)
        yaml.add_constructor(u'!dice', dice_constructor)

        dice = yaml.load("""initial hit points: !dice 8d4""")

        print(dice)

        pattern = re.compile(r'^\d+d\d+$')
        yaml.add_implicit_resolver(u'!dice', pattern)
        print(yaml.dump({'treasure': Dice(10, 20)}))


        d = yaml.load("""
        damage: 5d10
        """)
        print(d)


if __name__ == '__main__':
    unittest.main()

