class Cls {
      int _value = 1234;
      int _delta;
   public:
      Cls();
      Cls(int);
      int get_value ();
};

Cls::Cls() : _delta(0) { };
Cls::Cls(int delta) : _delta(delta) { };

int Cls::get_value () {
   return _value + _delta;
}
