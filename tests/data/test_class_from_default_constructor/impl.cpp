class Cls {
      int value = 1234;
   public:
      Cls();
      int get_value ();
};

Cls::Cls() { };

int Cls::get_value () {
   return value;
}
