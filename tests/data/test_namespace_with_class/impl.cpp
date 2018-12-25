namespace Outer {

   class Cls {
         int value = 1234;
      public:
         Cls();
         int get_value ();
   };
}
   
Outer::Cls::Cls() { };
   
int Outer::Cls::get_value () {
   return value;
}
