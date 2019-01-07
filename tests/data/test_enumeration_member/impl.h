class Cls {
   public:
      enum Elements { Invalid, Elem1, Elem2, Elem3 };
   private:
      Elements data;
   public:
      Cls();
      Cls(Elements e);
      Elements get();
      void set(Elements e);
};
