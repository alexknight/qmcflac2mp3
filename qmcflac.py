#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-25 20:00
# @Author  : alexknight
# @Site    : 
# @File    : qmcflac.py
# @Desc    :
import argparse
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
        self.qmc_files = self.__get_origin_files()
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

    def flac_to_mp3(self):
        if self.num == 0:
            self.__flac_to_mp3(self.flac_files, "/tmp/flac")
        else:
            print("使用线程池，将启动%d个线程" % self.num)
            groups = self.__chunks(self.flac_files, self.num)
            for i in range(self.num):
                p = multiprocessing.Process(target=self.__flac_to_mp3, args=(groups[i], "/tmp/flac-%s" % i))
                p.start()
                self.procs.append(p)

            for p in self.procs:
                p.join()

    def __get_origin_files(self):
        origin_files = []
        files = os.listdir(self.input)
        for file in files:
            if file.endswith(".qmcflac"):
                origin_files.append(os.path.join(self.input, file))
        return origin_files

    def __chunks(self, files, n):
        return [files[i:i + n] for i in range(0, len(files), n)]

    def __get_proc_num(self):
        size = len(self.qmc_files)
        num = int(size / 5)
        return num if num <= 8 else 8

    def __flac_to_mp3(self, flac_files, _tmp_dir):
        if os.path.exists(_tmp_dir):
            shutil.rmtree(_tmp_dir)
        os.mkdir(_tmp_dir)
        for path in flac_files:
            shutil.move(path, _tmp_dir)
        cmd = "%s %s %s" % (flac2mp3_tool, _tmp_dir, self.output)
        print(cmd)
        os.system(cmd)
        shutil.rmtree(_tmp_dir)
        print("%s flac_to_mp3 convert finish." % _tmp_dir)


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', type=os.path.abspath,
            help='need to convert')
    # options and flags
    parser.add_argument('-o', '--output-dir', type=os.path.abspath,
            help='Directory to output transcoded files to')

    parser.add_argument('-n', '--thread-num', type=int,
            help='convert thread num')

    args = parser.parse_args()

    if args.input_dir is not None:
        input_dir = args.input_dir
    else:
        raise Exception("please input correct input_dir.")

    if args.thread_num is not None:
        thread_num = args.thread_num
    else:
        thread_num = 0

    output_dir = args.output_dir
    convert = Convert(input=input_dir, output=output_dir, num=thread_num)
    convert.qmc_to_flac().flac_to_mp3()


if __name__ == '__main__':
    main()
