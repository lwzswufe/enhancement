#include <stdio.h>
#include "math.h"
#include "Python.h"
#include "structmember.h"
#define PY_SSIZE_T_CLEAN


/*
编译命令:
g++ Custom.h Custom.cpp -D_hypot=hypot -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python36 -o custom.pyd -shared -fPIC
add "-D_hypot=hypot" for error: '::hypot' has not been declared 
*/
/*
PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 的字段叫 ob_base ，
包含了一个指针指向类型对象和一个引用计数(这可以用宏 Py_REFCNT 和 Py_TYPE 来区分)。
用宏来抽象，使得附加字段可以用调试构建。
*/

// 定义模块信息
static PyModuleDef custommodule = 
{
    PyModuleDef_HEAD_INIT,
    .m_name = "custom",
    .m_doc = "Example module that creates an extension type.",
    .m_size = -1,
};

// 把函数声明为可以被Python调用，需要先定义一个方法表
// 定义成员函数 method table
// 注意第三个参数 ( METH_VARARGS ) ，这个标志指定会使用C的调用惯例。
// 可选值有 METH_VARARGS 、 METH_VARARGS | METH_KEYWORD
// 如果单独使用 METH_VARARGS ，函数会等待Python传来tuple格式的参数，并最终使用 PyArg_ParseTuple() 进行解析。
// METH_KEYWORDS 值表示接受关键字参数。这种情况下C函数需要接受第三个 PyObject * 对象，表示字典参数，
// 使用 PyArg_ParseTupleAndKeywords() 来解析出参数
// 这个方法表必须被模块定义结构所引用
// 定义成员函数
static PyMethodDef Custom_methods[2] = {};

// 定义成员变量
static PyMemberDef Custom_members[4] = {};

// Custom 类的对象 object 包含了： CustomObject 结构，这会为每个 Custom 实例分配一次。
typedef struct 
{
    PyObject_HEAD    // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
    PyObject *first; /* first name */
    PyObject *last;  /* last name */
    int number;
} CustomObject;
static char member_name_first[] = {"first"};
static char member_name_last[] = {"last"};
static char member_name_number[] = {"number"};

static char member_doc_first[] = {"first name"};
static char member_doc_last[] = {"last name"};
static char member_doc_number[] = {"number name"};

// 定义CustomType 结构体，其定义了一堆标识和函数指针，会指向解释器里请求的操作
// 定义Python类型
static PyTypeObject CustomType
{
    PyVarObject_HEAD_INIT(NULL, 0)  // 这一行是强制的样板 用于初始化 PyVarObject_HEAD_INIT(type, size)
};

// 定义Python对象函数 __del__()
static void Custom_dealloc(CustomObject *self)
{
    Py_XDECREF(self->first);                    // 减少引用计数
    Py_XDECREF(self->last);                     // 减少引用计数
    Py_TYPE(self)->tp_free((PyObject *) self);  // 释放对象
    printf("__del__()\n");
}

// 定义Python对象函数  __new__()
static PyObject * Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CustomObject *self;
    self = (CustomObject *) type->tp_alloc(type, 0);    // 构造新对象
    if (self != NULL)                                   // 为新对象赋值
    {
        self->first = PyUnicode_FromString("");
        if (self->first == NULL) 
        {
            Py_XDECREF(self);                           // new 对象失败 减少引用计数
            return NULL;
        }
        self->last = PyUnicode_FromString("");
        if (self->last == NULL) 
        {
            Py_XDECREF(self);                           // new 对象失败 减少引用计数
            return NULL;
        }
        self->number = 0;
    }
    printf("__new__()\n");
    return (PyObject *) self;                           // 返回 实例
}

// Python对象 初始化函数 __init__()
static int Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {member_name_first, 
                             member_name_last,
                             member_name_number, 
                             NULL};
    PyObject *first = NULL, *last = NULL, *tmp;
    // 解析构造函数参数
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
                                     &first, &last,
                                     &self->number))
        return -1;

    if (first)                  // 若原first值不为空
    {
        tmp = self->first;
        Py_INCREF(first);       // 增加 新赋值变量first的 引用计数
        self->first = first;
        Py_XDECREF(tmp);        // 减少 原变量的  引用计数
    }
    if (last)                   // 若原last值不为空
    {
        tmp = self->last;
        Py_INCREF(last);        // 增加 新赋值变量last的 引用计数
        self->last = last;
        Py_XDECREF(tmp);        // 减少 原变量的  引用计数
    }
    printf("__init__()\n");
    return 0;
}

// 定义Python对象函数
static PyObject * Custom_name(CustomObject *self, PyObject *Py_UNUSED(ignored))
{   // Py_UNUSED 这个可用于函数定义中未使用的参数以隐藏编译器警告
    if (self->first == NULL) 
    {
        PyErr_SetString(PyExc_AttributeError, member_name_first);
        return NULL;
    }
    if (self->last == NULL) 
    {
        PyErr_SetString(PyExc_AttributeError, member_name_first);
        return NULL;
    }
    return PyUnicode_FromFormat("%S %S", self->first, self->last);
}

// 模块初始化
// 这个结构体必须传递给解释器的模块初始化函数。初始化函数必须命名为 PyInit_name() ，
// 其中 name 是模块的名字，并应该定义为非 static ，且在模块文件里
PyMODINIT_FUNC PyInit_custom(void)
{
    PyObject *m;
    // 对模块函数列表进行初始化
    Custom_methods[0] = {"name", (PyCFunction) Custom_name, METH_NOARGS, "Return the name, combining the first and last name"};
    Custom_methods[1] = {NULL};
    // 对模块变量列表进行初始化
    Custom_members[0] = {member_name_first, T_OBJECT_EX, offsetof(CustomObject, first), 0, member_doc_first};
    Custom_members[1] = {member_name_last , T_OBJECT_EX, offsetof(CustomObject, last),  0, member_name_last};
    Custom_members[2] = {member_name_number, T_INT,     offsetof(CustomObject, number), 0, member_name_number};
    Custom_members[3] = {NULL};
    // 类型函数初始化
    CustomType.tp_name = "custom.Custom";     // 类型描述  __str__
    CustomType.tp_doc = "Custom objects";     // 文档 help调用
    CustomType.tp_basicsize = sizeof(CustomObject);
    CustomType.tp_itemsize = 0;
    CustomType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
    CustomType.tp_new = Custom_new;   // 等效于Python method __new__()  
    CustomType.tp_init = (initproc) Custom_init; // 初始化 __init__()
    CustomType.tp_dealloc = (destructor) Custom_dealloc; // 释放内存 __del__()
    CustomType.tp_members = Custom_members;   // 定义类变量
    CustomType.tp_methods = Custom_methods;   // 定义类方法

    if (PyType_Ready(&CustomType) < 0)
        return NULL;

    m = PyModule_Create(&custommodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&CustomType);
    if (PyModule_AddObject(m, "Custom", (PyObject *) &CustomType) < 0) {
        Py_XDECREF(&CustomType);
        Py_XDECREF(m);
        return NULL;
    }

    return m;
}