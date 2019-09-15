#include <stdio.h>

/*
编译动态链接库的路径:
gcc C_dll.c -o C_dll.so -shared -fPIC
*/
int add_func(int a,int b)
{   
    int c = a + b;
    printf("the result: %d\n", c);
    return c;
}
