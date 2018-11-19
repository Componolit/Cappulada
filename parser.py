#!/usr/bin/env python

import sys
import os
import traceback
import argparse
from capdpa import *

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outdir', help="target directory", default=os.path.abspath(os.curdir))
parser.add_argument('-p', '--project', help="project name", default="Capdpa")
parser.add_argument('headers', help="header files", nargs='+')

if __name__ == "__main__":

    args = sys.argv[1:sys.argv.index('--')] if '--' in sys.argv else sys.argv[1:]
    clang_args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = parser.parse_args(args)
    compilation_units = []

    for header in args.headers:
        try:
            compilation_units.extend(CXX(header, clang_args).ToIR(project=args.project).AdaSpecification())
        except:
            traceback.print_exc()

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
