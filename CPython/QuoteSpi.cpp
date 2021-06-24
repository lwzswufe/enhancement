#include <stdio.h>
#include <deque>
#include <vector>
#include "math.h"
#include "Python.h"
#include "structmember.h"
#define PY_SSIZE_T_CLEAN
#define CODE_SIZE 7

/*
编译命令:
Windows 打包为pyd文件
Linux   打包为so 文件
g++ QuoteSpi.cpp -D_hypot=hypot -I C:\\Anaconda3\\include -L C:\\Anaconda3 -l python3.7 -o QuoteSpi.pyd -shared -fPIC
g++ QuoteSpi.cpp -D_hypot=hypot -I /home/wiz/anaconda3/include/python3.8  -L /home/wiz/anaconda3/lib -l python3.8 -o QuoteSpi.so -shared -fPIC -std=c++11
g++ QuoteSpi.cpp -D_hypot=hypot -I /home/anaconda3/include/python3.7m  -L /home/anaconda3/lib -l python3.7m -o QuoteSpi.so -shared -fPIC -std=c++11
add "-D_hypot=hypot" for error: '::hypot' has not been declared 
参考 https://docs.python.org/3/extending/newtypes_tutorial.html?highlight=t_object_ex
*/
/*
PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 的字段叫 ob_base ，
包含了一个指针指向类型对象和一个引用计数(这可以用宏 Py_REFCNT 和 Py_TYPE 来区分)。
用宏来抽象，使得附加字段可以用调试构建。
*/


// 把函数声明为可以被Python调用，需要先定义一个方法表
// 定义成员函数 method table
// 注意第三个参数 ( METH_VARARGS ) ，这个标志指定会使用C的调用惯例。
// 可选值有 METH_VARARGS 、 METH_VARARGS | METH_KEYWORD
// 如果单独使用 METH_VARARGS ，函数会等待Python传来tuple格式的参数，并最终使用 PyArg_ParseTuple() 进行解析。
// METH_KEYWORDS 值表示接受关键字参数。这种情况下C函数需要接受第三个 PyObject * 对象，表示字典参数，
// 使用 PyArg_ParseTupleAndKeywords() 来解析出参数
// 这个方法表必须被模块定义结构所引用


// 定义MarketData成员函数
static PyMethodDef MarketData_methods[4] = {};

// 定义MarketData成员变量
static PyMemberDef MarketData_members[8] = {};

// 行情数据类的对象 object 包含了： MarketData 结构，这会为每个 MarketData 实例分配一次。
// C++调用类型 与 static PyTypeObject MarketDataType相关联
typedef struct MarketData
{
    PyObject_HEAD;   // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
    double last_pr;
    double  b1_pr;
    double  s1_pr;
    PyObject* code;
} MarketDataObject;

// 定义QuoteSpiType 结构体，其定义了一堆标识和函数指针，会指向解释器里请求的操作
// 定义Python类型 python调用的类型
static PyTypeObject MarketDataType
{
    PyVarObject_HEAD_INIT(NULL, 0)  // 这一行是强制的样板 用于初始化 PyVarObject_HEAD_INIT(type, size)
};

// 测试数据结构体 供C++读取文件使用
struct SimpleQuotaData
{
    char code[7];
    double last_pr;
    double b1_pr;
    double s1_pr;
};

// 此变量 不可声明为静态变量
std::deque<const SimpleQuotaData* > QueueMarketData{};


static void ReadData()
{   
    // 返回python列表 list
    FILE* fp = fopen("MarketData", "r");
    if (fp == nullptr)
        perror("error in open file\n");
    char line[1024];
    int count = 0;
    printf("read %d data, deque size:%lu \n", count, QueueMarketData.size());
    QueueMarketData.clear();
    printf("read %d data, deque size:%lu \n", count, QueueMarketData.size());
    while( fgets(line, 1024, fp))
    {   
        SimpleQuotaData* new_data = new SimpleQuotaData;
        strncpy(new_data->code, line, CODE_SIZE);
        new_data->code[CODE_SIZE - 1] = 0;
        int read_n = sscanf(line+7, "%lf,%lf,%lf", &(new_data->last_pr), &(new_data->b1_pr), &(new_data->s1_pr));
        // printf("read %s: %s,%.2lf,%.2lf,%.2lf\n", line, new_data->code, new_data->last_pr, new_data->b1_pr, new_data->s1_pr);
        QueueMarketData.push_back(new_data);
        ++count;
    }
    fclose(fp);
    printf("read %d data, deque size:%lu \n", count, QueueMarketData.size());
}

static PyObject * 
MarketData_str(MarketData* self, PyObject* args, PyObject *kwds)
{
    char s[256];
    sprintf(s, "str(): %s, %.2lf,%.2lf,%.2lf", PyUnicode_AsUTF8(self->code),
             self->last_pr, self->b1_pr,  self->s1_pr);
    PyObject* pString = PyUnicode_FromString(s);
    return pString;
}

// 定义Python对象函数 __del__()
static void MarketData_dealloc(MarketDataObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);  // 释放对象
    // printf("__del__()\n");
}

// 定义Python对象函数  __new__()
static PyObject * MarketData_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    MarketDataObject *self;
    self = (MarketDataObject *) type->tp_alloc(type, 0);     // 构造新对象
    if (self != NULL)                                   // 为新对象赋值
    {
    }
    // printf("__new__()\n");
    return (PyObject *) self;                           // 返回 实例
}

// Python对象 初始化函数 __init__()
static int MarketData_init(MarketDataObject *self, PyObject *args, PyObject *kwds)
{   
    return 0;
}

// 定义成员函数
static PyMethodDef BaseStrategy_methods[4] = {};

// 定义成员变量
static PyMemberDef BaseStrategy_members[4] = {};

//  QuoteSpi 类的对象 object 包含了： QuoteSpi 结构，这会为每个 QuoteSpi 实例分配一次。
typedef struct BaseStrategy
{
    PyObject_HEAD    // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
} BaseStrategyObject;

// 定义QuoteSpiType 结构体，其定义了一堆标识和函数指针，会指向解释器里请求的操作
// 定义Python类型
static PyTypeObject BaseStrategyType
{
    PyVarObject_HEAD_INIT(NULL, 0)  // 这一行是强制的样板 用于初始化 PyVarObject_HEAD_INIT(type, size)
};

// 定义Python对象函数 __del__()
static void BaseStrategy_dealloc(BaseStrategyObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);  // 释放对象
    printf("__del__()\n");
}

// 定义Python对象函数  __new__()
static PyObject * BaseStrategy_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    BaseStrategyObject *self;
    self = (BaseStrategyObject *) type->tp_alloc(type, 0);     // 构造新对象
    if (self != NULL)                                   // 为新对象赋值
    {
    }
    printf("__new__()\n");
    return (PyObject *) self;                           // 返回 实例
}

// Python对象 初始化函数 __init__()
static int BaseStrategy_init(BaseStrategyObject *self, PyObject *args, PyObject *kwds)
{   
    return 0;
}


// 回调函数
static PyObject* BaseStrategy_OnMarket(BaseStrategyObject* self, PyObject* args)
{   
     if (PyTuple_Size(args) == 0)
    {   
        printf("Strategy OnMarket error in arg parse\n");
        Py_RETURN_NONE;
    }
    else
    {   
        PyObject* pObj = PyTuple_GET_ITEM(args, 0);
        // printf("Strategy OnMarket arg parse success return stg:%p\n", pObj);
        if (pObj != nullptr)
        {   char s[512];
            MarketData* pData = (MarketData*)pObj;
            sprintf(s, "OnMarket code:%s last_pr:%.2lf b1_pr:%.2lf s1_pr:%.2lf\n", 
                PyUnicode_AsUTF8(pData->code), pData->last_pr, pData->b1_pr, pData->s1_pr);
        }
    }
    Py_RETURN_NONE;
}

// 定义成员函数
static PyMethodDef QuoteSpi_methods[4] = {};

// 定义成员变量
static PyMemberDef QuoteSpi_members[4] = {};

//  QuoteSpi 类的对象 object 包含了： QuoteSpi 结构，这会为每个 QuoteSpi 实例分配一次。
typedef struct QuoteSpi
{
    PyObject_HEAD    // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
    PyObject* StrategyList; // 策略列表
    std::vector<PyObject*> VecStg;
} QuoteSpiObject;

// 定义QuoteSpiType 结构体，其定义了一堆标识和函数指针，会指向解释器里请求的操作
// 定义Python类型
static PyTypeObject QuoteSpiType
{
    PyVarObject_HEAD_INIT(NULL, 0)  // 这一行是强制的样板 用于初始化 PyVarObject_HEAD_INIT(type, size)
};

// 定义Python对象函数 __del__()
static void QuoteSpi_dealloc(QuoteSpiObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);  // 释放对象
    printf("__del__()\n");
}

// 定义Python对象函数  __new__()
static PyObject * QuoteSpi_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    QuoteSpiObject *self;
    self = (QuoteSpiObject *) type->tp_alloc(type, 0);     // 构造新对象
    if (self != NULL)                                   // 为新对象赋值
    {
    }
    printf("__new__()\n");
    return (PyObject *) self;                           // 返回 实例
}

// Python对象 初始化函数 __init__()
static int QuoteSpi_init(QuoteSpiObject *self, PyObject *args, PyObject *kwds)
{   
    self->StrategyList = PyList_New(0);
    ReadData();
    return 0;
}

static PyObject* QuoteSpi_get(PyObject* self, PyObject* args)
{   
    if (QueueMarketData.empty())
        Py_RETURN_NONE;
    else
    {
        const SimpleQuotaData* pData = QueueMarketData[0];
        // printf("%s,%.2lf,%.2lf,%.2lf\n", pData->code, pData->last_pr, pData->b1_pr, pData->s1_pr);
        QueueMarketData.pop_front();
        // TYPE* PyObject_New(TYPE, PyTypeObject *type)
        // TYPE C类型
        // PyTypeObject Python类型
        // MarketData* pPyData = PyObject_NewVar(MarketData, &MarketDataType, sizeof(MarketData));
        MarketData* pPyData = PyObject_New(MarketData, &MarketDataType);
        // printf("before %p code:%p last_pr:%p b1_pr:%p s1_pr:%p\n", pPyData, pPyData->code, pPyData->last_pr, pPyData->b1_pr, pPyData->s1_pr);
        // 字符串 code
        pPyData->code = PyUnicode_FromString(pData->code);
        // 浮点型数据
        pPyData->last_pr = pData->last_pr;
        pPyData->b1_pr = pData->b1_pr;
        pPyData->s1_pr = pData->s1_pr;
        // printf("after  %p code:%p last_pr:%p b1_pr:%p s1_pr:%p\n", pPyData, pPyData->code, pPyData->last_pr, pPyData->b1_pr, pPyData->s1_pr);
        // printf("%.2lf,%.2lf,%.2lf\n", PyFloat_AsDouble(pPyData->last_pr),  PyFloat_AsDouble(pPyData->b1_pr),  PyFloat_AsDouble(pPyData->s1_pr));
        return (PyObject*)pPyData;
    }
}

// 注册策略
static PyObject* QuoteSpi_Register(QuoteSpiObject* self, PyObject* args)
{   
    printf("arg: %p\n", args);
    PyObject* pStg;
    if (PyTuple_Size(args) == 0)
    {   
        printf("spi register error in arg parse\n");
        Py_RETURN_FALSE;
    }
    else
    {   
        pStg = PyTuple_GET_ITEM(args, 0);
        printf("spi register arg parse success return stg:%p\n", pStg);
    }
    self->VecStg.push_back(pStg);
    // 类型检查
    if (PyList_Append(self->StrategyList, pStg) >= 0)
    {   
        printf("spi register append strategy success\n");
        Py_RETURN_TRUE;
    }
    else
    {   
        printf("spi register error in arg parse\n");
        Py_RETURN_FALSE;
    }
}

// 运行策略策略
static PyObject* QuoteSpi_Start(QuoteSpiObject* self, PyObject* args)
{   
    while(!QueueMarketData.empty())
    {
        const SimpleQuotaData* pData = QueueMarketData[0];
        // printf("%s,%.2lf,%.2lf,%.2lf\n", pData->code, pData->last_pr, pData->b1_pr, pData->s1_pr);
        QueueMarketData.pop_front();
        // TYPE* PyObject_New(TYPE, PyTypeObject *type)
        // TYPE C类型
        // PyTypeObject Python类型
        // MarketData* pPyData = PyObject_NewVar(MarketData, &MarketDataType, sizeof(MarketData));
        MarketData* pPyData = PyObject_New(MarketData, &MarketDataType);
        // printf("before %p code:%p last_pr:%p b1_pr:%p s1_pr:%p\n", pPyData, pPyData->code, pPyData->last_pr, pPyData->b1_pr, pPyData->s1_pr);
        // 字符串 code
        pPyData->code = PyUnicode_FromString(pData->code);
        // 浮点型数据
        pPyData->last_pr = pData->last_pr;
        pPyData->b1_pr = pData->b1_pr;
        pPyData->s1_pr = pData->s1_pr;
        // for (int i=0; i< PyList_Size(self->StrategyList); ++i)
        // {
        //     PyObject* PyObj = PyList_GET_ITEM(self->StrategyList, i);
        //     PyObject_CallMethod(PyObj, "OnMarket", "O", pPyData);
        // }
        for (PyObject* PyObj: self->VecStg)
        {
            PyObject_CallMethod(PyObj, "OnMarket", "O", pPyData);
        }
        // printf("data:%p\n", pPyData);
    }
    Py_RETURN_FALSE;
}

// 定义模块信息
static PyModuleDef Quotemodule = 
{
    PyModuleDef_HEAD_INIT,
    .m_name = "QuoteSpi",
    .m_doc = "Example module that creates an extension type.",
    .m_size = -1
};

// 模块初始化
// 这个结构体必须传递给解释器的模块初始化函数。初始化函数必须命名为 PyInit_name() ，
// 其中 name 是模块的名字，并应该定义为非 static ，且在模块文件里
PyMODINIT_FUNC PyInit_QuoteSpi(void)
{
    PyObject *m;
    //
    /*
    Field	C Type	        Meaning
    name	const char *	name of the member
    type	int	            the type of the member in the C struct
    offset	Py_ssize_t	    the offset in bytes that the member is located on the type’s object struct
    flags	int	            flag bits indicating if the field should be read-only or writable
    doc	    const char *	points to the contents of the docstring
    */
   // 结构体的各个元素在结构体里的位置
   printf("offset: code:%lu last_pr:%lu b1_pr:%lu s1_pr:%lu\n", offsetof(MarketData, code), 
        offsetof(MarketData, last_pr), offsetof(MarketData, b1_pr), offsetof(MarketData, s1_pr));
    // 定义类变量
    MarketData_members[0] = {"code", T_OBJECT_EX, offsetof(MarketData, code),  0, "code[6] like 600000"}; 
    MarketData_members[1] = {"last_pr", T_DOUBLE, offsetof(MarketData, last_pr),  0, "last price"}; 
    MarketData_members[2] = {"b1_pr", T_DOUBLE, offsetof(MarketData, s1_pr),  0, "bid 1 price"}; 
    MarketData_members[3] = {"s1_pr",T_DOUBLE, offsetof(MarketData, b1_pr),  0, "ask 1 price"}; 
    MarketData_members[4] = { NULL }; 

    MarketData_methods[0] = {"str", (PyCFunction)MarketData_str, METH_NOARGS, "str"};
    MarketData_methods[1] = { NULL };
    
    MarketDataType.tp_name = "QuoteSpi.MarketData";     // 类型描述  __str__
    MarketDataType.tp_doc = "MarketData objects";     // 文档 help调用
    MarketDataType.tp_basicsize = sizeof(MarketData);
    MarketDataType.tp_itemsize = 0;
    MarketDataType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
    MarketDataType.tp_new = MarketData_new;   // 等效于Python method __new__()  
    MarketDataType.tp_init = (initproc) MarketData_init; // 初始化 __init__()
    MarketDataType.tp_dealloc = (destructor) MarketData_dealloc; // 释放内存 __del__()
    MarketDataType.tp_members = MarketData_members;   // 定义类变量
    MarketDataType.tp_methods = MarketData_methods;

    if (PyType_Ready(&MarketDataType) < 0)
        return NULL;

    // 定义类变量
    BaseStrategy_members[0] = { NULL }; 
    // 定义类方法
    BaseStrategy_methods[0] = {"OnMarket", (PyCFunction)BaseStrategy_OnMarket, METH_VARARGS, "OnMarket"};
    BaseStrategy_methods[1] = { NULL };
    
    BaseStrategyType.tp_name = "QuoteSpi.BaseStrategy";     // 类型描述  __str__
    BaseStrategyType.tp_doc = "BaseStrategy objects";     // 文档 help调用
    BaseStrategyType.tp_basicsize = sizeof(BaseStrategy);
    BaseStrategyType.tp_itemsize = 0;
    BaseStrategyType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
    BaseStrategyType.tp_new = BaseStrategy_new;   // 等效于Python method __new__()  
    BaseStrategyType.tp_init = (initproc) BaseStrategy_init; // 初始化 __init__()
    BaseStrategyType.tp_dealloc = (destructor) BaseStrategy_dealloc; // 释放内存 __del__()
    BaseStrategyType.tp_members = BaseStrategy_members;   // 定义类变量
    BaseStrategyType.tp_methods = BaseStrategy_methods;

    if (PyType_Ready(&BaseStrategyType) < 0)
        return NULL;

     // 对模块函数列表进行初始化 
    QuoteSpi_methods[0] = {"get", (PyCFunction) QuoteSpi_get, METH_NOARGS, "get data"};
    QuoteSpi_methods[1] = {"Register", (PyCFunction)QuoteSpi_Register, METH_VARARGS, "Register"};
    QuoteSpi_methods[2] = {"Start", (PyCFunction) QuoteSpi_Start, METH_NOARGS, "Start"};
    QuoteSpi_methods[3] = {NULL};
    // 对模块变量列表进行初始化
    QuoteSpi_members[0] = {"StrategyList", T_OBJECT_EX, offsetof(QuoteSpi, StrategyList),  0, "StrategyList"}; 
    QuoteSpi_members[1] = {NULL};
    // 类型函数初始化
    QuoteSpiType.tp_name = "Quote.QuoteAPI";     // 类型描述  __str__
    QuoteSpiType.tp_doc = "Quote objects";     // 文档 help调用
    QuoteSpiType.tp_basicsize = sizeof(QuoteSpiObject);
    QuoteSpiType.tp_itemsize = 0;
    QuoteSpiType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
    QuoteSpiType.tp_new = QuoteSpi_new;   // 等效于Python method __new__()  
    QuoteSpiType.tp_init = (initproc) QuoteSpi_init; // 初始化 __init__()
    QuoteSpiType.tp_dealloc = (destructor) QuoteSpi_dealloc; // 释放内存 __del__()
    QuoteSpiType.tp_members = QuoteSpi_members;   // 定义类变量
    QuoteSpiType.tp_methods = QuoteSpi_methods;   // 定义类方法

    if (PyType_Ready(&QuoteSpiType) < 0)
        return NULL;

    m = PyModule_Create(&Quotemodule);
    if (m == NULL)
        return NULL;
    // 添加类型到模块
    Py_INCREF(&MarketDataType);
    if (PyModule_AddObject(m, "MarketData", (PyObject *) &MarketDataType) < 0) 
    {
        Py_XDECREF(&MarketDataType);
        Py_XDECREF(m);
        return NULL;
    }
    Py_INCREF(&BaseStrategyType);
    if (PyModule_AddObject(m, "BaseStrategy", (PyObject *) &BaseStrategyType) < 0) 
    {
        Py_XDECREF(&BaseStrategyType);
        Py_XDECREF(m);
        return NULL;
    }
    Py_INCREF(&QuoteSpiType);
    if (PyModule_AddObject(m, "QuoteSpi", (PyObject *) &QuoteSpiType) < 0) 
    {
        Py_XDECREF(&QuoteSpiType);
        Py_XDECREF(m);
        return NULL;
    }
    QueueMarketData.clear();
    return m;
}