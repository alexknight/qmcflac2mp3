#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-06-25 20:00
# @Author  : shefferliao
# @Site    : 
# @File    : qmcflac.py.py
# @Desc    :
import argparse
import os
import shutil

root_path = os.path.abspath(os.path.dirname(__file__))
qmc2flac_tool = os.path.join(root_path, "tools/qmc2flac/decoder")
flac2mp3_tool = os.path.join(root_path, "tools/flac2mp3/flac2mp3.pl")


class Convert(object):
    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output if output is not None else input
        self.qmc_files = self.__get_origin_files()
        self.flac_files = []
        self.mp3_files = []

    def __get_origin_files(self):
        origin_files = []
        files = os.listdir(self.input)
        for file in files:
            if file.endswith(".qmcflac"):
                origin_files.append(os.path.join(self.input, file))
        return origin_files

    def qmc_to_flac(self):
        os.chdir(self.input)
        cmd = qmc2flac_tool
        print(cmd)
        os.system(cmd)
        self.flac_files = [x.replace(".qmcflac", ".flac") for x in self.qmc_files]
        print("qmc_to_flac convert finish.")
        return self

    def flac_to_mp3(self):
        _tmp_dir = "/tmp/flac"
        if not os.path.exists(_tmp_dir):
            os.mkdir(_tmp_dir)
        for path in self.flac_files:
            shutil.move(path, _tmp_dir)
        cmd = "%s %s %s" % (flac2mp3_tool, _tmp_dir, self.output)
        print(cmd)
        os.system(cmd)
        shutil.rmtree(_tmp_dir)
        print("flac_to_mp3 convert finish.")


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', type=os.path.abspath,
            help='need to convert')
    # options and flags
    parser.add_argument('-o', '--output-dir', type=os.path.abspath,
            help='Directory to output transcoded files to')

    args = parser.parse_args()

    if args.input_dir is not None:
        input_dir = args.input_dir
    else:
        raise Exception("please input correct input_dir.")
    output_dir = args.output_dir
    convert = Convert(input=input_dir, output=output_dir)
    convert.qmc_to_flac().flac_to_mp3()


if __name__ == '__main__':
    main()
