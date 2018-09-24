with With_Class.In_Namespace;
package Full
is
   type Class is
   tagged limited record
      Value : With_Class.In_Namespace.In_Namespace;
      Value_Ptr : access With_Class.In_Namespace.In_Namespace;
   end record
   with Import, Convention => CPP;
   function Constructor return Class;
   pragma Cpp_Constructor (Constructor, "");
end Full;
