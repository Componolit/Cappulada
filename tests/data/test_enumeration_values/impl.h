enum Elements { Negative = -5000, Invalid = 17, Elem1 = 119, Elem2 = 5, Elem3 = 1, Big = 4294967295 };

class Cls {
   private:
      Elements data;
   public:
      Cls();
      Cls(Elements e);
      Elements get();
      void set(Elements e);
};
