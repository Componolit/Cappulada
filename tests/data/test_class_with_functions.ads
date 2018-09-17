package With_Functions is
   type With_Functions is
   tagged limited record
      null;
   end record
   with Import => CPP;
   procedure Public_Function (Arg1 : Integer);
   with Import, Convention => CPP, External_Name => "";
   function Named_Param (Param : Integer) return Integer
   with Import, Convention => CPP, External_Name => "";
   function Constructor return With_Functions;
   pragma Cpp_Constructor (Constructor, "");
end With_Functions;
