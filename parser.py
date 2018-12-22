#!/usr/bin/env python

import sys
import os
import traceback
import argparse
from capdpa import *

# Default with mix-in
with_defaults='''
with Interfaces.C;
'''

# Default spec mix-in
spec_defaults='''
   subtype Bool is Interfaces.C.int;
   subtype Unsigned_Char is Interfaces.C.unsigned_char;
   subtype Unsigned_Short is Interfaces.C.unsigned_short;
   subtype Unsigned_Int is Interfaces.C.unsigned;
   subtype Unsigned_Long is Interfaces.C.unsigned_long;
   --  unsigned long long is not defined in Interfaces.C
   subtype Char is Interfaces.C.char;
   subtype Signed_Char is Interfaces.C.signed_char;
   subtype Wchar_t is Interfaces.C.wchar_t;
   subtype Short is Interfaces.C.short;
   subtype Int is Interfaces.C.int;
   --  __int128/unsigned __int128 is not defined in Interfaces.C
   subtype Long is Interfaces.C.long;
   --  long long is not defined in Interfaces.C
   subtype C_float is Interfaces.C.C_float;
   subtype Double is Interfaces.C.double;
   subtype Long_Double is Interfaces.C.long_double;
'''

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outdir', help="target directory", default=os.path.abspath(os.curdir))
parser.add_argument('-p', '--project', help="project name", default="Capdpa")
parser.add_argument('-s', '--spec_include', help="specification include")
parser.add_argument('-w', '--with_include', help="with include")
parser.add_argument('headers', help="header files", nargs='+')

if __name__ == "__main__":

    args = sys.argv[1:sys.argv.index('--')] if '--' in sys.argv else sys.argv[1:]
    clang_args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = parser.parse_args(args)
    compilation_units = []

    if args.with_include is not None:
        with open(args.with_include, 'r') as wi:
            with_include = wi.read ()
    else:
        with_include = with_defaults

    if args.spec_include is not None:
        with open(args.spec_include, 'r') as si:
            spec_include = si.read ()
    else:
        spec_include = spec_defaults

    for header in args.headers:
        try:
            compilation_units.extend(CXX(header, clang_args).ToIR(project=args.project,
                                                                  with_include=with_include,
                                                                  spec_include=spec_include).AdaSpecification())
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
