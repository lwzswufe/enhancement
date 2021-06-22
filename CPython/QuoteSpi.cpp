#include <stdio.h>
#include <deque>
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
g++ QuoteSpi.cpp -D_hypot=hypot -I /home/wiz/anaconda3/include/python3.8  -L /home/wiz/anaconda3/lib -l python3.8 -o QuoteSpi.so -shared -fPIC
g++ QuoteSpi.cpp -D_hypot=hypot -I /home/anaconda3/include/python3.7m  -L /home/wiz/anaconda3/lib -l python3.7m -o QuoteSpi.so -shared -fPIC
add "-D_hypot=hypot" for error: '::hypot' has not been declared 
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
// 定义成员函数
static PyMethodDef QuoteSpi_methods[4] = {};

// 定义成员变量
static PyMemberDef QuoteSpi_members[8] = {};


// 定义MarketData成员函数
static PyMethodDef MarketData_methods[4] = {};

// 定义MarketData成员变量
static PyMemberDef MarketData_members[4] = {};

// 行情数据类的对象 object 包含了： MarketData 结构，这会为每个 MarketData 实例分配一次。
struct MarketDataType
{
    PyObject_HEAD;   // PyObject_HEAD 是强制要求必须在每个对象结构体之前，用以定义一个类型为 PyObject 
                     // 的字段叫 ob_base ，包含了一个指针指向类型对象和一个引用计数
    PyObject* code;
    PyObject* last_pr;
    PyObject* b1_pr;
    PyObject* s1_pr;
};

// 测试数据结构体
struct SimpleQuotaData
{
    char code[7];
    double last_pr;
    double b1_pr;
    double s1_pr;
};

static std::deque<const SimpleQuotaData* > QueueMarketData{};
static MarketDataType DATA{};
// 读取测试数据
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

static PyObject* ReadData(PyObject* self, PyObject* args)
{   
    // 返回python列表 list
    FILE* fp = fopen(filename, "r");
    if (fp == nullptr)
        perror("error in open file\n");
    char line[1024];
    while( fgets(line, 1024, fp))
    {   
        SimpleQuotaData* new_data = new SimpleQuotaData;
        strncpy(new_data->code, line, CODE_SIZE);
        new_data->code[CODE_SIZE - 1] = 0;
        int read_n = sscanf(line+7, "%lf,%lf,%lf", &(new_data->last_pr), &(new_data->b1_pr), &(new_data->s1_pr));
        // printf("read %s: %s,%.2lf,%.2lf,%.2lf\n", line, new_data->code, new_data->last_pr, new_data->b1_pr, new_data->s1_pr);
        QueueMarketData.put(new_data);
    }
    fclose(fp);
    return pList;
}

static PyObject* GetData(PyObject* self, PyObject* args)
{   
    if (QueueMarketData.empty())
        Py_RETURN_NONE;
    else
    {
        const SimpleQuotaData* pData = QueueMarketData[0];
        QueueMarketData.pop_front();
        
        // 字符串 code
        DATA.code = PyBytes_FromString(pData->code)
        // 浮点型数据 timenum d_vol tradevol total_sell_vol
        DATA.last_pr = PyFloat_FromDouble(pData->last_pr);
        DATA.b1_pr = PyFloat_FromDouble(pData->b1_pr);
        DATA.s1_pr = PyFloat_FromDouble(pData->s1_pr);
        return &DATA;
    }
}
// 定义模块方法表
// 第一个字段：在 Python 里面使用的方法名；
// 第二个字段：C 模块内的函数名；
// 第三个字段：方法参数类型，是无参数(METH_NOARGS) , 还是有位置参数(METH_VARARGS), 还是其他等等；
// 第四个字段：方法描述，就是通过 help() 或者 doc 可以看到的
// 类的所有成员函数结构列表同样是以全NULL结构结束
static PyMethodDef Module_MethodMembers[4]
{
    { "Read", (PyCFunction)ReadData, METH_VARARGS, "read data" },
    { "Get", (PyCFunction)ReadData, METH_VARARGS, "read data" },
    { NULL, NULL, 0, NULL }
};

// 定义模块信息
static PyModuleDef Quotemodule = 
{
    PyModuleDef_HEAD_INIT,
    .m_name = "Quote",
    .m_doc = "Example module that creates an extension type.",
    .m_size = -1,
    .m_methods = Module_MethodMembers
};

// 模块初始化
// 这个结构体必须传递给解释器的模块初始化函数。初始化函数必须命名为 PyInit_name() ，
// 其中 name 是模块的名字，并应该定义为非 static ，且在模块文件里
PyMODINIT_FUNC PyInit_Quote(void)
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
    // 定义类变量
    MarketData_members[0] = {"code", T_OBJECT_EX, setoffsetof(MarketDataType, code),  READONLY, "code[6] like 600000"}; 
    MarketData_members[1] = {"last_pr", T_DOUBLE, setoffsetof(MarketDataType, last_pr),  READONLY, "last price"}; 
    MarketData_members[2] = {"b1_pr", T_DOUBLE, setoffsetof(MarketDataType, b1_pr),  READONLY, "bid 1 price"}; 
    MarketData_members[3] = {"s1_pr",T_DOUBLE, setoffsetof(MarketDataType, s1_pr),  READONLY, "ask 1 price"}; 
    MarketData_members[4] = { NULL }; 

    MarketData_methods[0] = { NULL };
    
    MarketDataType.tp_name = "QuoteSpi.MarketData";     // 类型描述  __str__
    MarketDataType.tp_doc = "MarketData objects";     // 文档 help调用
    MarketDataType.tp_basicsize = sizeof(MarketDataType);
    MarketDataType.tp_itemsize = 0;
    MarketDataType.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
    MarketDataType.tp_members = MarketData_members;   // 定义类变量
    MarketDataType.tp_methods = MarketData_methods;

    if (PyType_Ready(&MarketDataType) < 0)
        return NULL;

    m = PyModule_Create(&Quotemodule);
    if (m == NULL)
        return NULL;
    // 添加类型到模块
    Py_INCREF(&MarketDataType);
    if (PyModule_AddObject(m, "MarketData", (PyObject *) &MarketDataType) < 0) {
        Py_XDECREF(&MarketDataType);
        Py_XDECREF(m);
        return NULL;
    }

    return m;
}