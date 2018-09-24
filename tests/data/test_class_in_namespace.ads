package With_Class.In_Namespace
is
   type Class is
   tagged limited record
      null;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end With_Class.In_Namespace;
