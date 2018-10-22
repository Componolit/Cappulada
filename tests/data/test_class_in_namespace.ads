package Capdpa.With_Class.In_Namespace
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.With_Class.In_Namespace;
