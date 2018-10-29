package Capdpa.From_Virtual
is
   type Class is new Capdpa.With_Virtual with
   limited record
      V : Capdpa.Int;
   end record
   with Import, Convention => CPP;
   type Private_Class is limited null record
   with Size => Class'Size;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Capdpa.From_Virtual;
