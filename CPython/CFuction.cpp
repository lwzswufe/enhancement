#include "Python.h"
#include <string.h>
#include <stdlib.h>
#include "structmember.h"
#define PY_SSIZE_T_CLEAN
#define PYTHON_API_VERSION 1013
/*
g++ CFuction.h CFuction.cpp -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python37 -o CFuction.pyd -shared -fPIC
g++ CFuction.cpp -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python37 -o CFuction.pyd -shared -fPIC
*/

// extern PyObject* ReadBars(PyObject* args, PyObject* kwds);


static PyObject* Range(PyObject* self, PyObject* args)
{   
    // 返回python列表 list
    int n{0};
    int ok = PyArg_ParseTuple(args, "i", &n); // 解析输入参数
    if (ok == 0)
    {
        return NULL;
    }
    PyObject *pList = PyList_New(0);
    for (int i=0; i<n; i++)
    {   
        PyList_Append(pList, Py_BuildValue("i", i));
    }
    return pList;
}

// 定义模块方法表
// 第一个字段：在 Python 里面使用的方法名；
// 第二个字段：C 模块内的函数名；
// 第三个字段：方法参数类型，是无参数(METH_NOARGS) , 还是有位置参数(METH_VARARGS), 还是其他等等；
// 第四个字段：方法描述，就是通过 help() 或者 doc 可以看到的
static PyMethodDef CFuction_MethodMembers[] =      //类的所有成员函数结构列表同样是以全NULL结构结束
{
      { "Range", (PyCFunction)Range, METH_VARARGS, "return list(Range(n))" },
      { NULL, NULL, 0, NULL }
};

// 定义模块信息
static PyModuleDef CFuction_ModuleInfo = 
{
    PyModuleDef_HEAD_INIT,
    .m_name = "CFuction",
    .m_doc = "Example module that creates an extension type.",
    .m_size = -1,
    .m_methods = CFuction_MethodMembers
};

// 初始化模块
PyMODINIT_FUNC PyInit_CFuction(void)      // 模块外部名称为--CFuction
{   
    PyObject* pReturn = 0;
    pReturn = PyModule_Create2(&CFuction_ModuleInfo, PYTHON_API_VERSION);  // 创建模块
    if (pReturn == NULL)
    {   
        printf("failed create module CFuction\n");
        return NULL;
    }
    else
    {
        printf("successful create module CFuction\n");
    }
    PyObject* ret = PyModuleDef_Init(&CFuction_ModuleInfo);    // 模块初始化
    if (ret == NULL)
    {   
        printf("failed initial module CFuction\n");
        return NULL;
    }
    else
    {
        printf("successful initial module CFuction\n");
    }
    return pReturn;
}