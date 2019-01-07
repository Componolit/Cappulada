class Base {
   public:
      Base();
      Base(int val);
      int parent();
      int parent_member;
};

class Cls : Base {
   public:
      Cls();
      Cls(int val);
      int local();
      int local_member;
};
