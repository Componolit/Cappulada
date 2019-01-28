# Cappulada

Cappulada is a tool to generate Ada bindings for C++. It aims to support complex features such as object orientation and templates while keeping a semantically appropriate mapping of namespaces and classes in C++ to packages and types in Ada.

## Function and Features

Cappulada uses libclang to parse C++ headers. It converts clangs abstract syntax tree into a custom intermediate representation. While this is still a tree based structure it gets enriched with further information:

- C++ linker symbols
- Instances of C++ templates
- Parent relations in the tree

The intermediate representation is a tree of classes, functions, types, etc. Each of these entities own a function to generate Ada specification snippets. When Ada code is generated the generator traverses the tree and combines those snippets into complete specification files. The specifications are aimed to be SPARK compatible as far as it is possible.

The generated Ada code resides in child packages of a single project package. This project package provides basic builtin types and hosts C++ code that resides in the `::` namespace. To provide a type mapping between C++ and Ada it depends on Adas `Interfaces.C` package.

The currently supported C++ features include

- Namespaces and Class
- Class functions, static functions, member variables
- Class inheritance with and without virtual functions
- Function pointers
- Templates

This list is not exhaustive, of course. Also there are many corner cases that currently aren't working properly. Array support has not yet been implemented, too. So there's still a long list of todos:

- Array support
- properly handling all clang AST types
- Crashes on specific template usages
- visibility issues

To get a more detailed view check out the [Version 1.0 Project](https://github.com/Componolit/Cappulada/projects/1).

## Installation

Install dependencies via

- `apt install python-clang-3.8 libclang-3.8-dev`
- `pip install -r requirements.txt`



## Tests

Since the tests include validation tests to check if the generated code compiles the [GNAT Toolchain](https://www.adacore.com/download/) is required to run the tests.

Run the tests via `python -m unittest discover tests`.



## Usage

The `cappulada` tool takes C++ headers as arguments. Furthermore a project name and a output path can be given. If arguments need to be passed to clang a `--` can be appended as an argument. Anything after that will be directly passed to clang.

```
usage:
	cappulada [-h] [-o OUTDIR] [-p PROJECT] headers [headers ...]

flags:
	-h			show help

options:
	-o			Output directory for Ada specs
	-p			Project name, also the name of the base package in Ada
```

### Example

A header residing in `/cppproject/` named `a.h` can be converted to `/adaproject` via

```
cappulada -p cappulada -o /adaproject /cppproject/a.h
```

If for example `a.h` looks as follows:

```C++
class A
{
    public:
        A();
        int add(int x, int y);
};
```

Cappulada will generate a project specification file, in this case named `cappulada.ads` and a package for class `A` named `cappulada-a.ads` with the following contents:

```Ada
package Cappulada.A
   with SPARK_Mode => On
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;

   type Class_Address is private;

   function Constructor return Class
   with Global => null;
   pragma Cpp_Constructor (Constructor, "_ZN1AC1Ev");

   function Add (This : Class; X : Cappulada.Int; Y : Cappulada.Int) return Cappulada.Int
   with Global => null, Import, Convention => CPP, External_Name => "_ZN1A3addEii";

private
   pragma SPARK_Mode (Off);

   type Class_Address is access Class;

end Cappulada.A;
```

In an Ada project this class can be used easily:

```Ada
with Ada.Text_Io;
with Cappulada.A;

procedure Main is
   X : Integer := 1;
   Y : Integer := 2;
   A : Cappulada.A.Class := Cappulada.A.Constructor;
begin
   Ada.Text_Io.Put_Line (Integer'Image (A.Add(X, Y)));
end Main;
```



