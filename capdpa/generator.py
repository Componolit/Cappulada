import sys
import os
import traceback
from capdpa import CXX
import clang.cindex

class InvalidProjectName(Exception): pass

# Default with mix-in
with_defaults='''
with Interfaces.C;
with Interfaces.C.Extensions;
'''

# Default spec mix-in
spec_defaults='''
   subtype Bool is Interfaces.C.Extensions.bool;
   subtype Unsigned_Char is Interfaces.C.unsigned_char;
   subtype Unsigned_Short is Interfaces.C.unsigned_short;
   subtype Unsigned_Int is Interfaces.C.unsigned;
   subtype Unsigned_Long is Interfaces.C.unsigned_long;
   subtype Unsigned_Long_Long is Interfaces.C.Extensions.unsigned_long_long;
   subtype Char is Interfaces.C.char;
   subtype Signed_Char is Interfaces.C.signed_char;
   subtype Wchar_t is Interfaces.C.wchar_t;
   subtype Short is Interfaces.C.short;
   subtype Int is Interfaces.C.int;
   subtype C_int128 is Interfaces.C.Extensions.Signed_128;
   --  unsigned __int128 is not defined in Interfaces.C.Extensions
   subtype Long is Interfaces.C.long;
   subtype Long_Long is Interfaces.C.Extensions.long_long;
   subtype C_float is Interfaces.C.C_float;
   subtype Double is Interfaces.C.double;
   subtype Long_Double is Interfaces.C.long_double;
'''

class Generator:

    def __init__(self, project, outdir, headers, clang_args=None, with_include=None, spec_include=None):

        if project.lower() == "class" or project.lower() == "constructor":
            raise InvalidProjectName()

        self.project    = project
        self.outdir     = outdir
        self.headers    = headers
        self.clang_args = clang_args or []

        if with_include is not None:
            with open(with_include, 'r') as wi:
                self.with_include = wi.read ()
        else:
            self.with_include = with_defaults

        if spec_include is not None:
            with open(spec_include, 'r') as si:
                spec_include = si.read ()
        else:
            self.spec_include = spec_defaults

    def run(self):

        compilation_units = []

        for header in self.headers:
            try:
                compilation_units.extend(CXX(header, self.clang_args).ToIR(project=self.project,
                                                                           with_include=self.with_include,
                                                                           spec_include=self.spec_include).AdaSpecification())
            except CXX.LoadError:
                raise
            except CXX.ParseError:
                raise
            except:
                traceback.print_exc()

        ud = {hash(cu.Text() + cu.FileName()):cu for cu in compilation_units}
        compilation_units = [ud[ch] for ch in set(ud.keys())]

        if len(set([cu.FileName() for cu in compilation_units])) != len(compilation_units):
            raise RuntimeError("Multiple different specifications of the same module")

        outdir = os.path.abspath(self.outdir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        for cu in compilation_units:
            with open(outdir + "/" + cu.FileName(), 'w') as cuf:
                cuf.write(cu.Text())
