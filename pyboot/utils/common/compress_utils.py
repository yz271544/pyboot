#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: compress_utils.py
@author: etl
@time: Created on 11/25/21 2:01 PM
@env: Python @desc:
@ref: @blog:
"""
import os
import gzip
import tarfile
import zipfile


def un_gz(file_full_name, target_dir):
    """
    gz
    因为gz一般仅仅压缩一个文件，全部常与其它打包工具一起工作。比方能够先用tar打包为XXX.tar,然后在压缩为XXX.tar.gz
    解压gz，事实上就是读出当中的单一文件，Python方法例如以下：
    :param file_full_name:
    :param target_dir
    :return:
    """
    """ungz gz file"""
    if os.path.isdir(target_dir):
        pass
    else:
        os.mkdir(target_dir)
    f_name = file_full_name.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(file_full_name)
    # 创建gzip对象
    open(os.path.join(target_dir, os.path.basename(f_name)), "wb+").write(g_file.read())
    # gzip对象用read()打开后，写入open()建立的文件里。
    g_file.close()
    # 关闭gzip对象


def un_tar(file_full_name, target_dir):
    """
    XXX.tar.gz解压后得到XXX.tar，还要进一步解压出来。

    *注：tgz与tar.gz是同样的格式，老版本号DOS扩展名最多三个字符，故用tgz表示。

    因为这里有多个文件，我们先读取全部文件名称。然后解压。例如以下：
    :param file_full_name:
    :param target_dir
    :return:
    """
    """untar tar file"""
    tar = tarfile.open(file_full_name)
    names = tar.getnames()
    if os.path.isdir(target_dir):
        pass
    else:
        os.mkdir(target_dir)
    # 因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar.extract(name, target_dir)
    tar.close()


def un_zip(file_full_name, target_dir):
    """
    与tar类似，先读取多个文件名称，然后解压。例如以下：
    :param file_full_name:
    :param target_dir:
    :return:
    """
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_full_name)
    if os.path.isdir(target_dir):
        pass
    else:
        os.mkdir(target_dir)
    for names in zip_file.namelist():
        zip_file.extract(names, target_dir)
    zip_file.close()


def in_tar(source_dir, target_full_tar):
    """
    tar打包
    在写打包代码的过程中，使用tar.add()添加文件时，会把文件本身的路径也加进去，加上arcname就能依据自己的命名规则将文件添加tar包

    在打包的过程中能够设置压缩规则,如想要以gz压缩的格式打包
    tar=tarfile.open('/path/to/your.tar.gz','w:gz')
    :param source_dir:  /path/to/dir/
    :param target_full_tar: /path/to/your.tar
    :return:
    """
    tar = tarfile.open(target_full_tar, 'w')
    for root, dir, files in os.walk(source_dir):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath, arcname=file)
    tar.close()
