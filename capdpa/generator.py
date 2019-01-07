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
   Bool_Size : constant := Bool'Size;
   type Bool_Address is access all Bool;

   subtype Unsigned_Char is Interfaces.C.unsigned_char;
   Unsigned_Char_Size : constant := Unsigned_Char'Size;
   type Unsigned_Char_Address is access all Unsigned_Char;

   subtype Unsigned_Short is Interfaces.C.unsigned_short;
   Unsigned_Short_Size : constant := Unsigned_Short'Size;
   type Unsigned_Short_Address is access all Unsigned_Short;

   subtype Unsigned_Int is Interfaces.C.unsigned;
   Unsigned_Int_Size : constant := Unsigned_Int'Size;
   type Unsigned_Int_Address is access all Unsigned_Int;

   subtype Unsigned_Long is Interfaces.C.unsigned_long;
   Unsigned_Long_Size : constant := Unsigned_Long'Size;
   type Unsigned_Long_Address is access all Unsigned_Long;

   subtype Unsigned_Long_Long is Interfaces.C.Extensions.unsigned_long_long;
   Unsigned_Long_Long_Size : constant := Unsigned_Long_Long'Size;
   type Unsigned_Long_Long_Address is access all Unsigned_Long_Long;

   subtype Char is Interfaces.C.char;
   Char_Size : constant := Char'Size;
   type Char_Address is access all Char;

   subtype Signed_Char is Interfaces.C.signed_char;
   Signed_Char_Size : constant := Signed_Char'Size;
   type Signed_Char_Address is access all Signed_Char;

   subtype Wchar_t is Interfaces.C.wchar_t;
   Wchar_t_Size : constant := Wchar_t'Size;
   type Wchar_t_Address is access all Wchar_t;

   subtype Short is Interfaces.C.short;
   Short_Size : constant := Short'Size;
   type Short_Address is access all Short;

   subtype Int is Interfaces.C.int;
   Int_Size : constant := Int'Size;
   type Int_Address is access all Int;

   subtype C_X_Int128 is Interfaces.C.Extensions.Signed_128;
   C_X_Int128_Size : constant := 128;
   type C_X_Int128_Address is access all C_X_Int128;

   --  unsigned __int128 is not defined in Interfaces.C.Extensions

   subtype Long is Interfaces.C.long;
   Long_Size : constant := Long'Size;
   type Long_Address is access all Long;

   subtype Long_Long is Interfaces.C.Extensions.long_long;
   Long_Long_Size : constant := Long_Long'Size;
   type Long_Long_Address is access all Long_Long;

   subtype C_float is Interfaces.C.C_float;
   C_float_Size : constant := C_float'Size;
   type C_float_Address is access all C_float;

   subtype Double is Interfaces.C.double;
   Double_Size : constant := Double'Size;
   type Double_Address is access all Double;

   subtype Long_Double is Interfaces.C.long_double;
   Long_Double_Size : constant := Long_Double'Size;
   type Long_Double_Address is access all Long_Double;

   subtype Void_Address is Interfaces.C.Extensions.void_ptr;
   Void_Address_Size : constant := Long_Integer'Size;
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
