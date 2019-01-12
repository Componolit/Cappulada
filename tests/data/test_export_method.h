#define is_ada __attribute__((annotate("ada")))

class Cls {
   public:
      int method (int param) is_ada;
};
