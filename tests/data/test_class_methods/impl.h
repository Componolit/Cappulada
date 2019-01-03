class Cls {
      int int_member;
      float float_member;
      bool bool_member;
      unsigned long ul_member;
      short short_member;
   public:
      Cls();
      Cls(int, float, bool, unsigned long, short);
      void get(int&, float&, bool&, unsigned long&, short&);
};
