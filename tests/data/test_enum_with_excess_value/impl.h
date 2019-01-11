enum Elements { Negative = -9223372036854775807, Invalid = 17, Elem1 = 119, Elem2 = 5, Elem3 = 1, Big = 9223372036854775807 };
// enum Elements { Negative = -9223372036854775808, Invalid = 17, Elem1 = 119, Elem2 = 5, Elem3 = 1, Big = 9223372036854775807 };

class Cls {
   private:
      Elements data;
   public:
      Cls();
      Cls(Elements e);
      Elements get();
      void set(Elements e);
};
