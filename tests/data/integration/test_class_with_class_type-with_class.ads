package Test_Class_With_Class_Type.With_Class
   with SPARK_Mode => On
is
   package In_Namespace
      with SPARK_Mode => On
   is
      type Class is
      limited record
         null;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN10With_class12In_namespaceC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end In_Namespace;

end Test_Class_With_Class_Type.With_Class;
