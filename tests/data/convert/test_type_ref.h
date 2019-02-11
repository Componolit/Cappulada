
struct Tr
{ };

template <typename T1, typename T2, typename T3, int T4, typename T5, char T6, bool T7>
struct Tt
{ };

template <>
struct Tt<Tr, int, Tr, 4, Tr, 't', true>
{ };

class T
{
    public:
        Tt<Tr, int, Tr, 4, Tr, 't', true> t;
};

