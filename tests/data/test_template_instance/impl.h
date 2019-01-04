template <typename T>
class Cls {
      T _data;
   public:
      Cls();
      Cls(T val);
      void get(T &val);
};

namespace Foo {
   Cls<char> cls_inst1('x');
   Cls<int> cls_inst2(1);
};
