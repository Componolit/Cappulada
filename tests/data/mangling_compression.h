namespace Root
{
   class Data {
      public:
         int elem;
   };

   class Cls {
      public:
         int no_compression (int p1, int p2) { };
         Data compression1 (int p1, Data p2) { };
         int compression2 (Data p1, int p2, Data p3) { };
   };
}
