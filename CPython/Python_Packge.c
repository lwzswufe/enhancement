#include "Python.h"
#define PYTHON_API_VERSION 1013
#define PYTHON_API_STRING "1013"

/*
编译成pyd文件
gcc Python_Packge.c -shared -o c_module.pyd -fPIC -I C:\\Anaconda3\\include -L C:\\Anaconda3 -lpython37
*/

int add_func(int a,int b) 
{
    return a+b;
}


static PyObject *_add_func(PyObject *self, PyObject *args)
{
    int _a,_b;
    int res;

    if (!PyArg_ParseTuple(args, "ii", &_a, &_b))
        return NULL;
    res = add_func(_a, _b);
    return PyLong_FromLong(res);
}

/*
struct PyMethodDef {
    const char  *ml_name;   / The name of the built-in function/method /
    PyCFunction ml_meth;    / The C function that implements it /
    int         ml_flags;   / Combination of METH_xxx flags, which mostly
                               describe the args expected by the C func /
    const char  *ml_doc;    / The __doc__ attribute, or NULL /
};
typedef struct PyMethodDef PyMethodDef;
*/
static PyMethodDef CppModuleMethods = 
{
    "add_func",
    _add_func,
    METH_VARARGS,
    "__doc__"
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "add_func",
    NULL,
    -1,
    SpamMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC initcpp_module(void) 
{
    PyObject *m;
    struct PyMethodDef *cmm = &CppModuleMethods;
    m = PyModule_Create2(cmm, "DADQWD");
    if (!m) {
        return NULL;
    }
    return m;
}