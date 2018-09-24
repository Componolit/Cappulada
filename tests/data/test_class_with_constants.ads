package With_Constants
is
   One : constant := 1;
   Two : constant := 2;
   Three : constant := 3;
   type Negative is (Minus_One, Minus_Two, Minus_Three);
   for Negative use (Minus_One => -1, Minus_Two => -2, Minus_Three => -3);
   type Class is
   tagged limited type
      null;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end With_Constants;
