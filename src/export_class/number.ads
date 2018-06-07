package Number is

   package Class_Number is
      type Number is limited record
         x : aliased Integer;  -- number.h:7
         y : aliased Integer;  -- number.h:7
      end record
      with
        Import,
        Convention => CPP;

      function New_Number (arg1 : Integer; arg2 : Integer) return Number;  -- number.h:11
      pragma CPP_Constructor (Entity => New_Number, External_Name => "_ZN6NumberC1Eii");

      function add (this : access Number) return Integer  -- number.h:12
      with
        Export,
        Convention => CPP,
        External_Name => "_ZN6Number3addEv";
   end;
   use Class_Number;
end Number;
