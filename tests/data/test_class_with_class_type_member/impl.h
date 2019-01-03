class Inner {
      int data;
   public:
      Inner();
      Inner(int d);
      int get_data();
};

class Outer {
   public:
      Outer();
      Outer(short d, int i);
      Inner class_data;
      short data;
      int get_inner_data();
};
