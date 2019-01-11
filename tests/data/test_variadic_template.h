template <typename A, typename B>
class Templ
{
   public:
      Templ() { };
      A element1;
      B element2;
};

template <typename ...Ts>
class Var
{
   public:
      Var() { };
      int element1;
//      void foo(Ts...);
};

class Cls
{
   public:
      Cls() { };
      int bar (Templ<char, int> p1, char p2) { return 0; };
      int foo (int p1, char p2) { return 0; };
      int baz (Templ<char, int> p1, Templ<char,char> p2) { return 0; };
      int var (Var<> p1, char p2) { return 0; };
};
