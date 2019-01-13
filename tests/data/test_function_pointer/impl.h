class Cls {
   public:
      Cls();
      void set_func(int (*arg)(int));
      int (*func) (int);
      int use_func(int);
};
