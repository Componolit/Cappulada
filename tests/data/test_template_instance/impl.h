template <typename T>
class Cls {
      T _data;
   public:
      Cls();
      Cls(T val1);
      void get(T &val2);
      T& get();
};

namespace Foo {
   Cls<char> cls_inst1('x');
   Cls<int> cls_inst2(1);
};
