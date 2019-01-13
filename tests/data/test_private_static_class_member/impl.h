class Cls {
      static short static_private;
   public:
      Cls();
      void set (short val);
      short get () __attribute__((annotate("ada")));
      static short static_public;
};
