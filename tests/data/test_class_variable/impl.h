class Cls {
   public:
      Cls();
      int value;
};

// This does not work:
// Cls Cls_inst1;

namespace Foo {
   Cls Cls_inst2;
};
