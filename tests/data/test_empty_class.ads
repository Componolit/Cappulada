package Empty is
   type Empty is
   tagged limited record
      null;
   end record
   with Import, Convention => CPP;
   function Constructor return Empty;
   pragma Cpp_Constructor (Constructor, "");
end Empty;
