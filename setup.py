#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: setup.py
@author: etl
@time: Created on 8/13/21 1:51 PM
@env: Python @desc:
@ref: @blog:
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyboot',  # How you named your package folder (foo)
    packages=['pyboot'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Convert web cookies to dictionary',  # Give a short description about your library
    author='huzhengyang',  # Type in your name
    author_email='huzhengyang@gridsum.com',  # Type in your E-Mail
    url='https://gitlab.gridsum.com/huzhengyang/pyboot',  # Provide either the link to your github or to your website
    download_url='https://gitlab.gridsum.com/huzhengyang/pyboot/archive/master.zip',
    keywords=['web-boot', 'server'],  # Keywords that define your package best
    install_requires=[
        "attrdict" == "2.0.1",
        "attrs" == "21.2.0",
        "cffi" == "1.14.6",
        "click" == "7.1.2",
        "dataclasses" == "0.8",
        "DBUtils" == "2.0.2",
        "Flask" == "1.1.4",
        "importlib-metadata" == "4.6.3",
        "iniconfig" == "1.1.1",
        "itsdangerous" == "1.1.0",
        "Jinja2" == "2.11.3",
        "MarkupSafe" == "2.0.1",
        "marshmallow" == "3.13.0",
        "marshmallow-objects" == "2.3.0",
        "packaging" == "21.0",
        "paho-mqtt" == "1.5.1",
        "pluggy" == "0.13.1",
        "py" == "1.10.0",
        "pycparser" == "2.20",
        "pyparsing" == "2.4.7",
        "pytest" == "6.2.4",
        "PyYAML" == "5.4.1",
        "six" == "1.16.0",
        "toml" == "0.10.2",
        "tornado" == "6.1",
        "typing-extensions" == "3.10.0.0",
        "Werkzeug" == "1.0.1",
        "zipp" == "3.5.0",
        "lightgbm" == "2.2.3",
        "numpy" == "1.17.4",
        "pandas" == "0.25.3",
        "scipy" == "1.4.0",
        "joblib" == "0.14.1",
        "scikit-image" == "0.16.2",
        "scikit-learn" == "0.20.3",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
