// windows: path C:\Anaconda3\include
// linux:   path \home\anaconda3\include
#include "Python.h"

/*
gcc C_Call_Python_2.c -o C_Call_Python_2.exe -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python36
gcc C_Call_Python_2.c -o C_Call_Python_2.exe -I /home/anaconda3/include/python3.7m -L /home/anaconda3/lib -l python3.7m
export LD_LIBRARY_PATH=/home/anaconda3/lib && ./C_Call_Python_2.exe
export PYTHONPATH=$PYTHONPATH:/home/anaconda3 && export LD_LIBRARY_PATH=/home/anaconda3/lib && ./C_Call_Python_2.exe
export PATH=/home/anaconda3/bin:$PATH && ./C_Call_Python_2.exe
windows 运行时需要把python36.dll拷贝到当前目录
*/

void show_python_version()
{
    // 设置解释器路径
    // Py_SetPythonHome(L"/home/anaconda3/bin");
    // Py_SetPath(L"/home/anaconda3:/home/anaconda3/bin/:/home/anaconda3/lib/:/home/anaconda3/include/:/home/anaconda3/include/python3.7m:.");
    // wchar_t* path = Py_GetPath();
    // wchar_t* home = Py_GetPythonHome();
    // printf("Python Path: %ls\nPython Home: %ls\n", path, home);
    /* 初始化解释器 */
    Py_Initialize();
    // 打印python版本信息
    PyRun_SimpleString("import sys;print(sys.version)");
    /* 结束解释器 */
    Py_Finalize();
}

long call_python_fun(long a) 
{
    long res = 1;
    PyObject *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    // Py_SetPath(L"/home/anaconda3:/home/anaconda3/lib:/home/anaconda3/bin");
    // Py_SetPythonHome(L"/home/anaconda3/bin");

    /* 初始化解释器 */
    Py_Initialize();
    // PyRun_SimpleFile("print('hello word')");
    // PyRun_SimpleString("print('Hello Python!')\n");
    /* 加载模块 */
    pModule = PyImport_ImportModule("python_file_exm");
    if (pModule == NULL)
    {   
        printf("error in import python file\n");
        return 0;
    }
    /* 获取函数对象 */
    pFunc = PyObject_GetAttrString(pModule, "python_function_exm"); 
    if (pFunc == NULL)
    {   
        printf("error in import python function\n");
        return 0;
    }
    /* 创建参数对象 size=1*/
    pArgs = PyTuple_New(1);
    /* 参数对象赋值 = 0*/
    PyTuple_SetItem(pArgs, 0, PyLong_FromLong(a));
    /* 调用函数 */
    pValue = PyObject_CallObject(pFunc, pArgs);
    /* 解析返回值 */
    res = PyLong_AsLong(pValue);
    /* 结束解释器 */
    Py_Finalize();
    printf("C get %d\n",res);
    return res;
}


const char* call_python_class(const char* str) 
{   
    const char* res{nullptr};
    PyObject *pModule, *pFunc;
    PyObject *pArgs, *pValue, *pObj, *pCls, *pDict, *pFun, *pIns;
    /* 初始化解释器 */
    Py_Initialize();
    /* 加载模块 */
    pModule = PyImport_ImportModule("python_file_exm");
    if (pModule == NULL)
    {   
        printf("error in import python file\n");
        return 0;
    }
    /* 加载模块方法字典 */
    pDict = PyModule_GetDict(pModule);
    if (pDict == nullptr)
    {
        printf("error in import python module dict\n");
        return nullptr;
    }
    /* 获取类型对象 */
    pCls = PyDict_GetItemString(pDict, "String"); 
    if (pCls == NULL || !PyCallable_Check(pCls))
    {   
        printf("error in import python Class\n");
        return 0;
    }
    /* 创建参数对象 size=1*/
    pArgs = PyTuple_New(1);
    /* 参数对象赋值 pos = 0*/
    int r = PyTuple_SetItem(pArgs, 0, PyBytes_FromString(str));
    printf("res:%d \n", r);
    /* 创建对象 */
    // pValue = PyObject_CallObject(pCls, pArgs);
    // pIns = PyObject_CallMethod(, "String", nullptr);
    pIns = PyObject_CallObject(pCls, nullptr);
    if (!pIns) 
    {
        printf("error create instance.\n");
        return 0;
    }
    printf("Instance:%p \n", pIns);
    /* 调用类方法 调用格式(实例 方法 参数1 参数2 NULL)*/
    // pValue = PyObject_CallMethod(pIns, "__str__", ""); 
    pValue = PyObject_CallMethodObjArgs(pIns, Py_BuildValue("s", "print"), Py_BuildValue("s", str), NULL);
    // pValue = PyObject_CallMethodObjArgs(pIns, "__str__", pArgs);
    printf("pObj:%p\n", pValue); 
    if (pValue == nullptr)
    {
        printf("error in call python Class\n");
        return 0;
    }
    // 解析数据
    res = PyUnicode_AsUTF8(pValue);
    printf("C get %p_%s\n", res, res);
    /* 结束解释器 */
    Py_Finalize();
    return res;
}


int main()
{   
    show_python_version();
    call_python_fun(1);
    call_python_fun(2);
    call_python_class("sda1");
    return 0;
}