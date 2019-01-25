package Test_Class_With_Struct_Type
   with SPARK_Mode => On
is
   package With_Struct
      with SPARK_Mode => On
   is
      package Ws
         with SPARK_Mode => On
      is
         type Class is
         limited record
            X : Test_Class_With_Struct_Type.Int;
         end record
         with Import, Convention => CPP;

         type Class_Address is private;

         function Constructor return Class
         with Global => null;
         pragma Cpp_Constructor (Constructor, "_ZN11With_Struct2WsC1Ev");

      private
         pragma SPARK_Mode (Off);

         type Class_Address is access Class;

      end Ws;
      package Ws2 is
         type Class is null record;
      end Ws2;
      type Class is
      limited record
         Value : Test_Class_With_Struct_Type.With_Struct.Ws.Class_Address;
         Value2 : Test_Class_With_Struct_Type.With_Struct.Ws2.Class_Address;
      end record
      with Import, Convention => CPP;

      type Class_Address is private;

      function Constructor return Class
      with Global => null;
      pragma Cpp_Constructor (Constructor, "_ZN11With_StructC1Ev");

   private
      pragma SPARK_Mode (Off);

      type Class_Address is access Class;

   end With_Struct;

end Test_Class_With_Struct_Type;
