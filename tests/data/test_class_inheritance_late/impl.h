class Base {
   public:
      Base();
      virtual int method();
      virtual int original();
      virtual int pure() = 0;
};

class Cls : Base {
   public:
      Cls();
      int method();
      int pure();
      int own();
};
