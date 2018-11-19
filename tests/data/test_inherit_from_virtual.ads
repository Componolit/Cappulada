package Capdpa.From_Virtual
is
   type Class is new Capdpa.With_Virtual with
   limited record
      V : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Class_Address is new System.Address;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.From_Virtual;
