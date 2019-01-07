class Outer {
   public:
      class Inner {
         public:
            Inner();
            Inner(int);
            int member;
            int method();
      };
      Outer();
      Outer(int);
      int member;
      int method();
};
