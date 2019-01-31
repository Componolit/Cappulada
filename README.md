# Cappulada

[![Build Status](https://travis-ci.org/Componolit/Cappulada.svg?branch=master)](https://travis-ci.org/Componolit/Cappulada)

Cappulada is a tool to generate Ada bindings for C++. It aims to support complex features such as object orientation and templates while keeping a semantically appropriate mapping of namespaces and classes in C++ to packages and types in Ada.

## Function and Features

Cappulada uses libclang to parse C++ headers. It converts clangs abstract syntax tree into a custom intermediate representation. While this is still a tree based structure it gets enriched with further information:

- C++ linker symbols
- Instances of C++ templates
- Parent relations in the tree

The intermediate representation is a tree of classes, functions, types, etc. Each of these entities own a function to generate Ada specification snippets. When Ada code is generated the generator traverses the tree and combines those snippets into complete specification files. The specifications are aimed to be SPARK compatible where possible.

The generated Ada code resides in child packages of a single project package. This project package provides basic builtin types and hosts C++ code that resides in the `::` namespace. To provide a type mapping between C++ and Ada it depends on Ada's `Interfaces.C` package.

The currently supported C++ features include

- Namespaces and Class
- Class functions, static functions, member variables
- Class inheritance with and without virtual functions
- Function pointers
- Templates

This list is not exhaustive. There are various corner cases that still need improvement. Array support has not been implemented, yet, but it is on our TODO list among other features:

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

The `example` directory contains an example using a C++ template in Ada. It consists of a C++ class that represents a number and implements methods to add another number and to get its value:

```C++
//number.h
template <typename T>
class Number
{
    private:
        T _value;
    public:
        Number(T v) : _value(v)
        { }

        void add(T n)
        {
            _value += n;
        }

        T value()
        {
            return _value;
        }
};
```

Cappulada currently only creates templates instances for templates that are used in C++ itself as it cannot collect them from Ada. Since this template is never used a dummy class has been added that uses the template.

```C++
class Dummy{
    public:
        Dummy(Number<int> n)
        {
            n.add(1);
            n.value();
        }
};
```

Now Cappulada recognizes an instance of `Number` that uses `int` and creates an according template instance. Since GCC only exports symbols of functions that are actually used into the binary each class method is called once. Otherwise the linker won't find them when linking against the Ada object.

To trigger GCC to create an object file a compilation unit is required. This is done via `number.cc` which needs to create an instance of `Dummy`:

````C++
//number.cc
#include <number.h>

Dummy d = Dummy(Number<int>(5));
````

To create an Ada binding for this small library Cappulada is called (in this case with the project name `Example`):

```
$ cappulada -P Example number.h
```

This creates a file called `example.ads`. It contains type definitions for standard C types and contains the two classes. The interesting part is the instantiated `Number` class that looks as follows in Ada:

```Ada
package Example is
   ...
   package Number_T_Int
      with SPARK_Mode => On
   is
      type Private_Int is limited private;
      type Private_Int_Address is limited private;

      type Class is
      limited record
         Private_X_Value : Private_Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor (V : Example.Int) return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN6NumberIiEC1Ei");

      procedure Add (This : Class; N : Example.Int)
      with Global => null, Import, Convention => CPP, External_Name => "_ZN6NumberIiE3addEi";

      function Value (This : Class) return Example.Int
      with Global => null, Import, Convention => CPP, External_Name => "_ZN6NumberIiE5valueEv";

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;
      type Private_Int is new Example.Int;
      type Private_Int_Address is access Private_Int;
   end Number_T_Int;
   ...
end Example;
```

Since Ada does not support compile time templates the class name is mangled. I contains a `_T` to show that it is a template instance and a `_Int` to show its instantiation type. To keep the memory layout all class members, public, protected and private are included in the class record. Yet only public members are given their original type. All others get a private type which cannot be assigned directly.

The class functions are imported into the package. Since those are member functions their first argument is the object (which is invisible in C++).

The example program that uses this library only adds two command line arguments and prints the output:

```Ada
with Ada.Command_Line;
with Ada.Text_Io;
with Example;
   
procedure Add is
   
   function Number_Add (X : Integer; Y : Integer) return Integer is
      A : Example.Number_T_Int.Class :=
         Example.Number_T_Int.Constructor (Example.Int(X));
   begin
      Example.Number_T_Int.Add (A, Example.Int (Y));
      return Integer(Example.Number_T_Int.Value (A));
   end Number_Add;
         
begin 
   if Ada.Command_Line.Argument_Count = 2 then
      Ada.Text_Io.Put_Line (Integer'Image (Number_Add (
         Integer'Value (Ada.Command_Line.Argument(1)),
         Integer'Value (Ada.Command_Line.Argument(2))
         )));
   end if; 
end Add;
```

It imports the Example package and can use the `Number` class natively in Ada. The interesting part happens in `Number_Add`. Since encapsulation and storage are different in Ada from C++ each package that resembles a C++ class has a Class type that stores the data. So an instance of number is of the type `Number_T_Int.Class` and the classes constructor is called via the package function `Number_T_Int.Constructor`. Since the same applies to class methods the first argument here needs to be the object itself. So a call to value (which has no arguments in C++) is transformed to `Number_T_Int.Value (A)` with `A` being the class object.

To try the example in this repository run:

```
$ cd example
$ ../cappulada -p Example number.h
$ make
$ ./add 1 1
```

