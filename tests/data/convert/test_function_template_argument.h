
namespace A{
    template <typename T>
    class Tp { };
}

namespace B{
    class G { };

    class F
    {
        public:
            void f(A::Tp<G>);
    };
}
