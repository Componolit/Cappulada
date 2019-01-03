class Cls {
      bool bool_member;
      unsigned char unsigned_char_member;
      unsigned short unsigned_short_member;
      unsigned unsigned_member;
      unsigned long unsigned_long_member;
      unsigned long long unsigned_long_long_member;
      char char_member;
      signed char signed_char_member;
      wchar_t wchar_t_member;
      short short_member;
      int int_member;
      __int128 int128_member;
      long long_member;
      long long long_long_member;
      float float_member;
      double double_member;
      long double long_double_member;
   public:
      Cls();

      Cls(bool b,
          unsigned char uc,
          unsigned short us,
          unsigned u,
          unsigned long ul,
          unsigned long long ull,
          char c,
          signed char sc,
          wchar_t wct,
          short s,
          int i,
          __int128 i128,
          long l,
          long long ll,
          float f,
          double d,
          long double ld);

      void get(bool &b,
               unsigned char &uc,
               unsigned short &us,
               unsigned &u,
               unsigned long &ul,
               unsigned long long &ull,
               char &c,
               signed char &sc,
               wchar_t &wct,
               short &s,
               int &i,
               __int128 &i128,
               long &l,
               long long &ll,
               float &f,
               double &d,
               long double &ld);
};
