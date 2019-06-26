#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-25 20:00
# @Author  : alexknight
# @Site    : 
# @File    : qmcflac.py
# @Desc    :
import argparse
import math
import os
import shutil
import multiprocessing

root_path = os.path.abspath(os.path.dirname(__file__))
qmc2flac_tool = os.path.join(root_path, "tools/qmc2flac/decoder")
flac2mp3_tool = os.path.join(root_path, "tools/flac2mp3/flac2mp3.pl")


class Convert(object):
    def __init__(self, input=None, output=None, num=0):
        self.input = input
        self.output = output if output is not None else input
        self.qmc_files = self.get_origin_files(suffix=".qmcflac")
        self.flac_files = []
        self.mp3_files = []
        self.procs =[]
        self.num = num if num != 0 else self.__get_proc_num()

    def qmc_to_flac(self):
        os.chdir(self.input)
        cmd = qmc2flac_tool
        print(cmd)
        os.system(cmd)
        self.flac_files = [x.replace(".qmcflac", ".flac") for x in self.qmc_files]
        print("qmc_to_flac convert finish.")
        return self

    def set_flac_files(self, files):
        self.flac_files = files
        return self

    def flac_to_mp3(self, save=False):
        if self.num == 0:
            self.__flac_to_mp3(self.flac_files, os.path.join(root_path, "flac"))
        else:
            print("使用线程池，将启动%d个线程" % self.num)
            groups = self.__chunks(self.flac_files, self.num)
            for i in range(len(groups)):
                p = multiprocessing.Process(target=self.__flac_to_mp3, args=(groups[i], os.path.join(root_path, "flac-%s" % i), save))
                p.start()

    def save(self, files):
        for file in files:
            shutil.move(file, self.output)

    def get_origin_files(self, suffix):
        origin_files = []
        files = os.listdir(self.input)
        for file in files:
            if file.endswith(suffix):
                origin_files.append(os.path.join(self.input, file))
        return origin_files

    def __chunks(self, files, n):
        size = len(files)
        list_size = int(math.ceil(size / n))
        return [files[i:i + list_size] for i in range(0, size, list_size)]

    def __get_proc_num(self):
        size = len(self.qmc_files)
        num = int(size / 5)
        return num if num <= 8 else 8

    def __flac_to_mp3(self, flac_files, _tmp_dir, save=False):
        if os.path.exists(_tmp_dir):
            shutil.rmtree(_tmp_dir)
        os.mkdir(_tmp_dir)
        for path in flac_files:
            if not save:
                shutil.move(path, _tmp_dir)
            else:
                shutil.copy(path, _tmp_dir)
        cmd = "%s %s %s" % (flac2mp3_tool, _tmp_dir, self.output)
        print(cmd)
        os.system(cmd)
        shutil.rmtree(_tmp_dir)
        print("%s flac_to_mp3 convert finish." % _tmp_dir)


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', type=os.path.abspath,
            help='need to convert')
    parser.add_argument('-o', '--output-dir', type=os.path.abspath,
            help='Directory to output transcoded files to')

    parser.add_argument('-m', '--mode', choices=('qmc2flac', 'flac2mp3', 'qmc2mp3'), default='qmc2flac')

    parser.add_argument('-n', '--thread-num', type=int,
            help='convert thread num')

    args = parser.parse_args()
    return args


def main():
    args = read_args()
    if args.input_dir is not None:
        input_dir = args.input_dir
    else:
        raise Exception("please input correct input_dir.")

    if args.thread_num is not None:
        thread_num = args.thread_num
    else:
        thread_num = 0

    mode = args.mode
    output_dir = args.output_dir

    convert = Convert(input=input_dir, output=output_dir, num=thread_num)
    if mode == 'qmc2mp3':
        convert.qmc_to_flac().flac_to_mp3()
    elif mode == 'qmc2flac':
        files = convert.qmc_to_flac().flac_files
        convert.save(files)
    elif mode == 'flac2mp3':
        files = convert.get_origin_files(suffix=".flac")
        convert.set_flac_files(files).flac_to_mp3(save=True)


if __name__ == '__main__':
    main()
