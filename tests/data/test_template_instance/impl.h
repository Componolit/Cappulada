template <typename T>
class Cls {
      T _data;
   public:
      Cls();
      Cls(T val);
      void get(T &val);
};

Cls<int> Cls_inst1;
Cls<char> Cls_inst2;
