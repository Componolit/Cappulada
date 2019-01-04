package Capdpa.With_Class.In_Namespace
is
   type Class is
   limited record
      null;
   end record
   with Import, Convention => CPP;
   type Class_Address is access Class;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "_ZN10With_class12In_namespaceC1Ev");
end Capdpa.With_Class.In_Namespace;
