//windows: path C:\Anaconda3\include
//linux:   sudo apt-get install python-dev 
#include "Python.h"


/*
gcc C_Call_Python_2.c -o C_Call_Python_2.exe -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python36
windows 运行时需要把python36.dll拷贝到当前目录
*/


long call_python_fun(long a) 
{
    long res = 1;
    PyObject *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    
    /* import */
    pModule = PyImport_ImportModule("python_file_exm");
    if (pModule == NULL)
    {   
        printf("error in import python file\n");
        return 0;
    }
    /* great_module.great_function */
    pFunc = PyObject_GetAttrString(pModule, "python_function_exm"); 
    if (pFunc == NULL)
    {   
        printf("error in import python function\n");
        return 0;
    }
    /* build args  size=1*/
    pArgs = PyTuple_New(1);
    /* set args pos = 0*/
    PyTuple_SetItem(pArgs, 0, PyLong_FromLong(a));
      
    /* call */
    // pValue = PyObject_CallObject(pFunc, pArgs);
    
    // res = PyLong_AsLong(pValue);
    printf("we input %d output %d\n", a, res);
    return res;
}

int main()
{
    call_python_fun(1);
    call_python_fun(2);
    return 0;
}