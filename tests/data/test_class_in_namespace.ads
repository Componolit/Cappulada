package With_Class.In_Namespace iis
   type In_Namespace is
   tagged limited record
      null;
   end record
   with => Import, Convention => CPP;
   function Constructor return In_Namespace;
   pragma Cpp_Constructor (Constructor, "");
end With_Class.In_Namespace;
