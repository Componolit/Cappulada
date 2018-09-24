package Empty
is
   type Class is
   tagged limited record
      null;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Empty;
