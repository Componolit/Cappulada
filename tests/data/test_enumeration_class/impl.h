class Cls {
   public:
      enum class Elements1 { Invalid, Elem1, Elem2, Elem3 };
      enum class Elements2 { Invalid, Elem1, Elem2, Elem3 };

      Elements1 member1;
      Elements2 member2;

      Cls();
      Cls(Elements1 initial);
};
