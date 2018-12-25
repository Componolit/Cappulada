class Cls {
      int _value = 1234;
      int _delta;
   public:
      Cls();
      Cls(int);
      Cls(int, int);
      int get_value ();
};

Cls::Cls() : _delta(0) { };
Cls::Cls(int delta) : _delta(delta) { };
Cls::Cls(int delta, int minus) : _delta(delta - minus) { };

int Cls::get_value () {
   return _value + _delta;
}
