class Cls {
      int _value;
   public:
      Cls();
      Cls(int val);
      __attribute__((annotate("ada"))) int ada_method (int param);
      int cpp_method (int param);
};
