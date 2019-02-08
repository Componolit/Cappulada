class Outer {
   private:
       class Inner
       {
          private:
             int i;
          public:
             Inner();
       };
       Inner ic;
   public:
       int o;
       Outer();
};
