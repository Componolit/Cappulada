
#include <stdio.h>
#include <stdlib.h>

#include <number.h>

int main(int argc, char *argv[])
{
    if (argc < 3)
        return 1;

    Number n(atoi(argv[1]), atoi(argv[2]));
    printf("%d\n", n.add());
    return 0;
}
