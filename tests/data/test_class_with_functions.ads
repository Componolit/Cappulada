   package Capdpa.With_Functions
      with SPARK_Mode => On
   is
      type Class is
      limited record
         null;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      procedure Public_Function (This : Class; Arg1 : Capdpa.Int)
      with Global => null, Import, Convention => CPP, External_Name => "_ZN14With_functions15public_functionEi";

      function Named_Param (This : Class; Param : Capdpa.Int) return Capdpa.Int
      with Global => null, Import, Convention => CPP, External_Name => "_ZN14With_functions11named_paramEi";

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN14With_functionsC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end Capdpa.With_Functions;
