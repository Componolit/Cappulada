with With_Class.In_Namespace;
package Full is
   type Full is
   tagged limited record
      Value : With_Class.In_Namespace.In_Namespace;
      Value_Ptr : access With_Class.In_Namespace.In_Namespace;
   end record
   with Import, Convention => CPP;
end Full;
