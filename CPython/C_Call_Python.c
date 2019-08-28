//windows: path C:\Anaconda3\include
//linux:   sudo apt-get install python-dev 
//https://docs.python.org/3/c-api/concrete.html#container-objects
#include "Python.h"

/*
gcc C_Call_Python.c -o C_Call_Python -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python36
windows 运行时需要把python36.dll拷贝到当前目录
*/

int main(int argc, char *argv[])
{
    //Py_SetProgramName(argv[0]);
    Py_Initialize();
    PyRun_SimpleString("print('Hello Python!')\n");
    Py_Finalize();
    printf("call over\n");
    return 0;
}
