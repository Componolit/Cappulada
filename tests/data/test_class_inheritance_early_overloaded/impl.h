class Base {
   private:
      int _member;
   public:
      Base();
      Base(int val);
      int method();
};

class Cls : Base {
   public:
      Cls();
      int method();
};
