package Test_Namespace_With_Class_With_Everything.With_Class
   with SPARK_Mode => On
is
   package With_Everything
      with SPARK_Mode => On
   is
      One : constant := 1;
      Two : constant := 2;
      type Negative is (Minus_Two, Minus_One)
      with Size => Test_Namespace_With_Class_With_Everything.Int'Size;
      for Negative use (Minus_Two => -2, Minus_One => -1);
      type Private_Int is limited private;
      type Private_Int_Address is limited private;

      type Class is
      limited record
         Private_Private_Int : Private_Int;
         Public_Int : Test_Namespace_With_Class_With_Everything.Int;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      procedure Public_Function (This : Class)
      with Global => null, Import, Convention => CPP, External_Name => "_ZN10With_class15With_everything15public_functionEv";

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN10With_class15With_everythingC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;
      type Private_Int is new Test_Namespace_With_Class_With_Everything.Int;
      type Private_Int_Address is access Private_Int;
   end With_Everything;

end Test_Namespace_With_Class_With_Everything.With_Class;
