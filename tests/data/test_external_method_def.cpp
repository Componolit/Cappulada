namespace Constants {
   class Cls {
      public:
         Cls ();
         void decl_only();
         void inline_def() { };
         void decl_and_def();
   };
};

void Constants::Cls::decl_and_def() { };
// void fun1(int param);
// void fun2(int param) { };
