#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>  
#include "C_Code_Exm.h"

/*
需要被Python调用的C代码 编译命令:
*/
int fac(int n)  
{  
    if (n < 2) return(1);  
    return (n)*fac(n-1);  
}  
  
char *reverse(char *s)  
{  
    char t,  
        *left = s,  
        *right = (s + (strlen(s) - 1));  
  
    while (s && (left < right))  
    {  
        t = *left;  
        *left++ = *right;  
        *right-- = t;  
    }  
    return s;  
}  
  
int test()  
{  
    char s[BUFSIZ];  
    printf("4! == %d\n", fac(4));  
    printf("8! == %d\n", fac(8));  
    printf("12! == %d\n", fac(12));  
    strncpy(s, "abcdef", BUFSIZ);  
    printf("reversing 'abcdef', we get '%s'\n", reverse(s));  
    strncpy(s, "madam", BUFSIZ);  
    printf("reversing 'madam', we get '%s'\n", reverse(s));  
    return 0;  
}  