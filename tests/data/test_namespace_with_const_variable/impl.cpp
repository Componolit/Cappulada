namespace Constants {
   enum { int_const = 42 };

   class Cls {
      public:
         int get_const ();
   };
};

int Constants::Cls::get_const() {
   return int_const;
}
