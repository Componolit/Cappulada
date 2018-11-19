#!/usr/bin/env python

import os
import argparse
from capdpa import *

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outdir', help="target directory", default=os.path.abspath(os.curdir))
parser.add_argument('-p', '--project', help="project name", default="Capdpa")
parser.add_argument('-c', '--clang', help="additional clang arguments")
parser.add_argument('headers', help="header files", nargs='+')

if __name__ == "__main__":
    args = parser.parse_args()
    compilation_units = []

    for header in args.headers:
        compilation_units.extend(CXX(header, args.clang.split(',') if args.clang else []).ToIR(project=args.project).AdaSpecification())

    ud = {hash(cu.Text() + cu.FileName()):cu for cu in compilation_units}
    compilation_units = [ud[ch] for ch in set(ud.keys())]

    if len(set([cu.FileName() for cu in compilation_units])) != len(compilation_units):
        raise RuntimeError("Multiple different specifications of the same module")

    outdir = os.path.abspath(args.outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for cu in compilation_units:
        with open(outdir + "/" + cu.FileName(), 'w') as cuf:
            cuf.write(cu.Text())
