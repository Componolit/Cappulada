package Capdpa.With_Virtual
is
   type Class is
   tagged limited record
      null;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
   procedure Foo
   with Import, Convention => CPP, External_Name => "";
end Capdpa.With_Virtual;
