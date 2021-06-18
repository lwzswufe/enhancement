#include <stdio.h>
#include <deque>
#include "math.h"
#include "Python.h"
#define PY_SSIZE_T_CLEAN


/*
编译命令:
Windows 打包为pyd文件
Linux   打包为so 文件
g++ Custom.cpp -D_hypot=hypot -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python3.7 -o Quote.pyd -shared -fPIC
g++ Custom.cpp -D_hypot=hypot -I /home/wiz/anaconda3/include/python3.8  -L /home/wiz/anaconda3/lib -l python3.8 -o Quote.so -shared -fPIC
g++ Custom.cpp -D_hypot=hypot -I /home/anaconda3/include/python3.7m  -L /home/wiz/anaconda3/lib -l python3.7m -o Quote.so -shared -fPIC
add "-D_hypot=hypot" for error: '::hypot' has not been declared 
*/
/*
PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 的字段叫 ob_base ，
包含了一个指针指向类型对象和一个引用计数(这可以用宏 Py_REFCNT 和 Py_TYPE 来区分)。
用宏来抽象，使得附加字段可以用调试构建。
*/

// 定义模块信息
static PyModuleDef Quotemodule = 
{
    PyModuleDef_HEAD_INIT,
    .m_name = "Quote",
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
static PyMethodDef Quote_methods[2] = {};

// 定义成员变量
static PyMemberDef Quote_members[4] = {};

// 行情数据类的对象 object 包含了： MarketData 结构，这会为每个 MarketData 实例分配一次。
struct MarketData
{
    PyObject_HEAD;   // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
    PyObject *code;  /* code */
    PyObject *last;  /* last price */
    PyObject *b1pr;  /* bid1 price */
    PyObject *s1pr;  /* ask1 price */
};

// Custom 类的对象 object 包含了： QuoteObject 结构，这会为每个 Custom 实例分配一次。
typedef struct QuoteAPI
{
    PyObject_HEAD    // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
} QuoteObject;

// 定义CustomType 结构体，其定义了一堆标识和函数指针，会指向解释器里请求的操作
// 定义Python类型
static PyTypeObject CustomType
{
    PyVarObject_HEAD_INIT(NULL, 0)  // 这一行是强制的样板 用于初始化 PyVarObject_HEAD_INIT(type, size)
};

// 定义Python对象函数 __del__()
static void Quote_dealloc(QuoteObject *self)
{
    Py_XDECREF(self->first);                    // 减少引用计数
    Py_XDECREF(self->last);                     // 减少引用计数
    Py_TYPE(self)->tp_free((PyObject *) self);  // 释放对象
    printf("__del__()\n");
}

// 定义Python对象函数  __new__()
static PyObject * Quote_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    QuoteObject *self;
    self = (QuoteObject *) type->tp_alloc(type, 0);     // 构造新对象
    if (self != NULL)                                   // 为新对象赋值
    {
    }
    printf("__new__()\n");
    return (PyObject *) self;                           // 返回 实例
}

// Python对象 初始化函数 __init__()
static int Quote_init(QuoteObject *self, PyObject *args, PyObject *kwds)
{
    return 0;
}

struct SimpleQuotaData
{
    char code[7];
    double last_pr;
    double b1_pr;
    double s1_pr;
    SimpleQuotaData* next;
};

static std::deque<SimpleQuotaData> QueueMarketData{};

SimpleQuotaData* ReadData(const char* filename)
{
    FILE* fp = fopen(filename, "r");
    if (fp == nullptr)
        perror("error in open file\n");
    char line[1024];
    SimpleQuotaData head{}, *temp{&head};
    head.next = nullptr;
    while( fgets(line, 1024, fp))
    {   
        SimpleQuotaData* new_data = new SimpleQuotaData;
        strncpy(new_data->code, line, CODE_SIZE);
        new_data->code[CODE_SIZE - 1] = 0;
        int read_n = sscanf(line+7, "%lf,%lf,%lf", &(new_data->last_pr), &(new_data->b1_pr), &(new_data->s1_pr));
        // printf("read %s: %s,%.2lf,%.2lf,%.2lf\n", line, new_data->code, new_data->last_pr, new_data->b1_pr, new_data->s1_pr);
        temp->next = new_data;
        temp = new_data;
        new_data->next = nullptr;
    }
    fclose(fp);
    return head.next;
}

// 定义Python对象函数
static PyObject * Quote_initial(QuoteObject *self, PyObject *args, PyObject *kwds)
{   // Py_UNUSED 这个可用于函数定义中未使用的参数以隐藏编译器警告
    static char *kwlist[] = {member_name_first, 
                             member_name_last,
                             NULL};
    const SimpleQuotaData *pData, *temp;
    pData = ReadData("MarketData");
    temp = pData;
    while (temp != nullptr)
    {
        printf("%s,%.2lf,%.2lf,%.2lf\n", temp->code, temp->last_pr, temp->b1_pr, temp->s1_pr);
        QueueMarketData.push_back(temp);
        temp = temp->next;
    }
    printf("quote initial over\n");
    Py_RETURN_NONE;
}

// 定义Python对象函数
static PyObject * Quote_run(QuoteObject *self, PyObject *args, PyObject *kwds)
{   // Py_UNUSED 这个可用于函数定义中未使用的参数以隐藏编译器警告
    static char *kwlist[] = {member_name_first, 
                             member_name_last,
                             NULL};
    const SimpleQuotaData *pData, *temp;
    pData = ReadData("MarketData");
    temp = pData;
    while (temp != nullptr)
    {
        printf("%s,%.2lf,%.2lf,%.2lf\n", temp->code, temp->last_pr, temp->b1_pr, temp->s1_pr);
        QueueMarketData.push_back(temp);
        temp = temp->next;
    }
    printf("quote initial over\n");
    Py_RETURN_NONE;
}

// 模块初始化
// 这个结构体必须传递给解释器的模块初始化函数。初始化函数必须命名为 PyInit_name() ，
// 其中 name 是模块的名字，并应该定义为非 static ，且在模块文件里
PyMODINIT_FUNC PyInit_Quote(void)
{
    PyObject *m;
    // 对模块函数列表进行初始化
    Quote_methods[0] = {"get_name", (PyCFunction) Quote_get_name, METH_NOARGS, "Return the name, combining the first and last name"};
    Quote_methods[1] = {"change_name", (PyCFunction) Quote_change_name, METH_VARARGS, "Change the name, first name and last name"};
    Quote_methods[2] = {NULL};
    // 对模块变量列表进行初始化
    Quote_members[0] = {member_name_first, T_OBJECT_EX, offsetof(QuoteObject, first), 0, member_doc_first};
    Quote_members[1] = {member_name_last , T_OBJECT_EX, offsetof(QuoteObject, last),  0, member_name_last};
    Quote_members[2] = {member_name_number, T_INT,     offsetof(QuoteObject, number), 0, member_name_number};
    Quote_members[3] = {NULL};
    // 类型函数初始化
    CustomType.tp_name = "Quote.Custom";     // 类型描述  __str__
    CustomType.tp_doc = "Custom objects";     // 文档 help调用
    CustomType.tp_basicsize = sizeof(QuoteObject);
    CustomType.tp_itemsize = 0;
    CustomType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
    CustomType.tp_new = Quote_new;   // 等效于Python method __new__()  
    CustomType.tp_init = (initproc) Quote_init; // 初始化 __init__()
    CustomType.tp_dealloc = (destructor) Quote_dealloc; // 释放内存 __del__()
    CustomType.tp_members = Quote_members;   // 定义类变量
    CustomType.tp_methods = Quote_methods;   // 定义类方法

    if (PyType_Ready(&CustomType) < 0)
        return NULL;

    m = PyModule_Create(&Quotemodule);
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