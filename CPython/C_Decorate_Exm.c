#include "Python.h"
#include "C_Code_Exm.h"

/*
C代码接口装饰文件 本文件用于装饰 C_Code_Exm.c 里的函数
接口的代码被称为“样板”代码，它是应用程序代码与Python解释器之间进行交互所必不可少的一部分。
样板主要分为4步：
    a、包含Python的头文件；
    b、为每个模块的每一个函数增加一个型如PyObject* Module_func()的包装函数；
    c、为每个模块增加一个型如PyMethodDef ModuleMethods[]的数组；
    d、增加模块初始化函数void initModule()
*/

static PyObject *  
cExm_fac(PyObject *self, PyObject *args)  
{  
    int num;  
    if (!PyArg_ParseTuple(args, "i", &num))  
        return NULL;  
    return (PyObject*)Py_BuildValue("i", fac(num));  
}  
  
static PyObject *  
cExm_doppel(PyObject *self, PyObject *args)  
{  
    char *orig_str;  
    char *dupe_str;  
    PyObject* retval;  
  
    if (!PyArg_ParseTuple(args, "s", &orig_str))  
        return NULL;  
    retval = (PyObject*)Py_BuildValue("ss", orig_str,  
        dupe_str=reverse(strdup(orig_str)));  
    free(dupe_str);             // 防止内存泄漏  
    return retval;  
}  
  
static PyObject *  
cExm_test(PyObject *self, PyObject *args)  
{  
    test();  
    return (PyObject*)Py_BuildValue("");  
}  
  
static PyMethodDef  
ExmMethods[] =  
{   
    // PyMethodDef 是一个 C结构体，用来完成一个映射，也就是便于方法查找，我们把需要被外面调用的方法都记录在这表内。
    // PyMethodDef 结构体成员说明：
    // 第一个字段：在 Python 里面使用的方法名；
    // 第二个字段：C 模块内的函数名；
    // 第三个字段：方法参数类型，是无参数(METH_NOARGS) , 还是有位置参数(METH_VARARGS), 还是其他等等；
    // 第四个字段：方法描述，就是通过 help() 或者 doc 可以看到的；

    { "fac", cExm_fac, METH_VARARGS, "int x = factor(int n)"},  
    { "doppel", cExm_doppel, METH_VARARGS, "reverse char s"},  
    { "test", cExm_test, METH_VARARGS, "for dll test"},  
    { NULL, NULL },  // 表示函数信息列表的结束
};  

static struct PyModuleDef cModPyDem =
{
    PyModuleDef_HEAD_INIT,
    "cExm", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    ExmMethods
};

PyMODINIT_FUNC PyInit_cExm(void)
{   
    // 这个函数名不能像上面那样，这是有规定的，必须是 init + 模块名字，比方说，我的最后编译出来的文件是
    // test.so, 那我的函数名就是 inittest, 这样在 Python 导入 test 模块时，才能找到这个函数并调用
    return PyModule_Create(&cModPyDem);
}