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
   type Bool_Address is access all Bool;

   subtype Unsigned_Char is Interfaces.C.unsigned_char;
   type Unsigned_Char_Address is access all Unsigned_Char;

   subtype Unsigned_Short is Interfaces.C.unsigned_short;
   type Unsigned_Short_Address is access all Unsigned_Short;

   subtype Unsigned_Int is Interfaces.C.unsigned;
   type Unsigned_Int_Address is access all Unsigned_Int;

   subtype Unsigned_Long is Interfaces.C.unsigned_long;
   type Unsigned_Long_Address is access all Unsigned_Long;

   subtype Unsigned_Long_Long is Interfaces.C.Extensions.unsigned_long_long;
   type Unsigned_Long_Long_Address is access all Unsigned_Long_Long;

   subtype Char is Interfaces.C.char;
   type Char_Address is access all Char;

   subtype Signed_Char is Interfaces.C.signed_char;
   type Signed_Char_Address is access all Signed_Char;

   subtype Wchar_t is Interfaces.C.wchar_t;
   type Wchar_t_Address is access all Wchar_t;

   subtype Short is Interfaces.C.short;
   type Short_Address is access all Short;

   subtype Int is Interfaces.C.int;
   type Int_Address is access all Int;

   subtype C_int128 is Interfaces.C.Extensions.Signed_128;
   type C_int128_Address is access all C_int128;

   --  unsigned __int128 is not defined in Interfaces.C.Extensions

   subtype Long is Interfaces.C.long;
   type Long_Address is access all Long;

   subtype Long_Long is Interfaces.C.Extensions.long_long;
   type Long_Long_Address is access all Long_Long;

   subtype C_float is Interfaces.C.C_float;
   type C_float_Address is access all C_float;

   subtype Double is Interfaces.C.double;
   type Double_Address is access all Double;

   subtype Long_Double is Interfaces.C.long_double;
   type Long_Double_Address is access all Long_Double;
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
            ir = CXX(header, self.clang_args).ToIR(project=self.project,
                                                   with_include=self.with_include,
                                                   spec_include=self.spec_include)
            compilation_units.extend(ir.AdaSpecification())

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
