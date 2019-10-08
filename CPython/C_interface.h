#include "Python.h"

extern int PyArg_ParseTuple(PyObject *arg, char *format, ...);
/*

arg参数必须是一个元组对象,它包含了从Python传递到C语言函数的参数列表。
format参数必须是格式字符串, 具体将在下方解释.其余参数必须是变量的地址,
其类型由格式字符串决定。为了能成功的转换,arg对象必须与格式匹配,并且前后
一一对应。

注意,虽然 PyArg_ParseTuple() 检查Python是否具有所需类型, 但是它不能
检查传递给调用的C变量地址的有效性: 如果在那里出错，您的代码可能会崩溃，
或者覆盖内存中的随机位置。所以要小心!

"s" (string or Unicode object) [char *]
将Python字符串或Unicode对象转换为指向字符串的C指针。不能为字符串本身提供存储;
指向现有字符串的指针存储在您传递地址的字符指针变量中。C字符串以NULL结尾。Python
字符串不能包含嵌入的空字节;如果有，就会引发TypeError异常。使用默认编码将Unicode
对象转换为C字符串。如果转换失败，就会引发一个UnicodeError异常。

"s#" (string,Unicode or any read buffer compatible object) [char *, int]
“s”上的这个变体存储在两个C变量中，第一个变量是指向字符串的指针，第二个变量是字符串的长度。
在这种情况下，Python字符串可能包含嵌入的空字节。如果可能的话，Unicode对象会返回一个指向
对象的默认编码字符串版本的指针。所有其他与读取缓冲区兼容的对象都将对原始内部数据表示的引用传回。

"z" (string or None) [char *]
与“s”类似，但是Python对象也可能是None，在这种情况下，C指针被设置为NULL。

"z#" (string or None or any read buffer compatible object) [char *, int]
这是"s#"就像"z"是"s"一样。

"u" (Unicode object) [Py_UNICODE *]
将Python Unicode对象转换为指向16位Unicode (UTF-16)数据的空端缓冲区的C指针。与“s”一样，不需要为Unicode数据缓冲区提供存储;指向现有Unicode数据的指针被存储到Py_UNICODE指针变量中，您传递的地址就是这个变量。

"u#" (Unicode object) [Py_UNICODE *, int]
“u”上的这个变体存储在两个C变量中，第一个变量是指向Unicode数据缓冲区的指针，第二个变量是它的长度。

"es" (string,Unicode object or character buffer compatible object) [const char *encoding,char **buffer]
这个“s”的变体用于编码Unicode和转换为Unicode的对象到字符缓冲区。它只适用于不嵌入空字节的编码数据。
读取一个变体C变量C和商店为两个变量,第一个指针指向一个编码名称字符串(encoding),第二个一个指向指针
的指针一个字符缓冲区(**buffer,缓冲用于存储编码数据)和第三个整数指针(*buffer_length,缓冲区长度)。
编码名称必须映射到已注册的编解码器。如果设置为NULL，则使用默认编码。
PyArg_ParseTuple()将使用PyMem_NEW()分配一个所需大小的缓冲区，将已编码的数据复制到这个缓冲区中，
并调整*buffer以引用新分配的存储。调用方负责调用PyMem_Free()以在使用后释放分配的缓冲区。

"es#" (string,Unicode object or character buffer compatible object) [const char *encoding,char **buffer, int *buffer_length]
这个“s#”的变体用于编码Unicode和转换为Unicode的对象到字符缓冲区。它读取一个C变量并存储到两个C变量,
第一个指针指向一个编码名称字符串(encoding),第二个一个指向指针的指针一个字符缓冲区(**buffer,缓冲
用于存储编码数据)和第三个整数指针(*buffer_length,缓冲区长度)。
编码名称必须映射到已注册的编解码器。如果设置为NULL，则使用默认编码。

操作方式有两种:

如果*buffer指向空指针，PyArg_ParseTuple()将使用PyMem_NEW()分配一个所需大小的缓冲区，将已编码
的数据复制到这个缓冲区，并调整*buffer以引用新分配的存储。调用方负责在使用后调用PyMem_Free()来
释放分配的缓冲区。

如果*buffer指向非空指针(已经分配的缓冲区)，PyArg_ParseTuple()将使用这个位置作为缓冲区，并将
*buffer_length解释为缓冲区大小。然后，它将把编码后的数据复制到缓冲区中，并终止(0-terminate)它。
缓冲区溢出以异常信号表示。

在这两种情况下，都将*buffer_length设置为编码数据的长度，没有后面的0字节(0-byte)。

"b" (integer) [char]
将Python整数转换为存储在C语言char中的一个小int(tiny int)。

"h" (integer) [short int]
将Python整数转换为C语言short int。

"i" (integer) [int]
将Python整数转换为普通的C语言int。

"l" (integer) [long int]
将Python整数转换为C语言long int。

"c" (string of length 1) [char]
将长度为1的字符串表示的Python字符转换为C语言char。

"f" (float) [float]
将Python浮点数转换为C语言float。

"d" (float) [double]
将Python浮点数转换为C 语言double。

"D" (complex) [Py_complex]
将Python复数转换为C语言Py_complex结构。

"O" (object) [PyObject *]
在C对象指针中存储Python对象(不进行任何转换)。因此，C程序接收传递的实际对象。
对象的引用计数没有增加。存储的指针不是空的(NULL)。

"O!" (object)[typeobject, PyObject *]
将Python对象存储在C对象指针中。这类似于“O”，但是接受两个C参数:第一个是Python
类型对象的地址，第二个是对象指针存储在其中的C变量(类型为PyObject *)的地址。如果
Python对象没有所需的类型，就会引发类型错误(TypeError)。
"O&" (object)[converter,anything]

通过转换器函数将Python对象转换为C变量。这需要两个参数:第一个是函数，第二个是C变量
(任意类型)的地址，转换为void *。该转换器功能依次调用如下:

    status = converter(object,address);

对象是要转换的Python对象，地址是传递给PyArg_ConvertTuple()的void *参数。对于成功的转换，
返回的状态应该是1，如果转换失败，则返回0。当转换失败时，converter(函数名可能错误)函数应该引发异常。

"S" (string) [PyStringObject *]
与“O”类似，但要求Python对象是字符串对象。如果对象不是字符串对象，则引发类型错误(TypeError)。
C变量也可以声明为PyObject *。

"U" (Unicode string) [PyUnicodeObject *]
与“O”类似，但要求Python对象是Unicode对象。如果对象不是Unicode对象，则引发类型错误(TypeError)。
C变量也可以声明为PyObject *。

"t#" (read-only character buffer) [char *, int]
与“s#”类似，但接受任何实现只读缓冲区接口的对象。char *变量设置为指向缓冲区的第一个字节，int设置
为缓冲区的长度。只接受单段缓冲对象;对所有其他类型都引发类型错误(TypeError)。

"w" (read-write character buffer) [char *]
类似于“s”，但接受任何实现读写缓冲区接口的对象。调用者必须通过其他方法确定缓冲区的长度，或者使用
“w#”。只接受单段缓冲对象;对所有其他类型都引发类型错误(TypeError)。

"w#" (read-write character buffer) [char *, int]
与“s#”类似，但接受任何实现读写缓冲区接口的对象。char *变量设置为指向缓冲区的第一个字节，int设置
为缓冲区的长度。只接受单段缓冲对象;对所有其他类型都引发类型错误(TypeError)。
"(items)" (tuple) [matching-items]
对象必须是一个Python序列，其长度是项中的格式单元数。C参数必须对应于项中的单个格式单元。序列的格式单元可以嵌套。
注意:在Python 1.5.2版本之前，这个格式说明符只接受包含单个参数的元组，而不是任意序列。以前导致在这里引发类型错误
(TypeError)的代码现在可以毫无例外地继续进行。对于现有的代码来说，这并不是一个问题。可以在请求整数的地方传递
Python长整数;然而，没有进行适当的范围检查——当接收字段太小而无法接收值时，最重要的位将被无声地截断(实际上，
语义是从C中的downcast继承来的——您的里程可能会有所不同(your mileage may vary))。

其他一些字符在格式字符串中有意义。这些可能不会发生在嵌套的括号中。它们是:

"|"
指示Python参数列表中的其余参数是可选的。与可选参数对应的C变量应该初始化为它们的默认值——当没有指定可选参数时，
PyArg_ParseTuple()不会触及相应的C变量(variable(s))的内容。

":"
格式单元列表在此结束;冒号后面的字符串用作错误消息中的函数名(PyArg_ParseTuple()引发的异常的“关联值
(associated value)”)。

";"
格式单元列表在此结束;冒号后面的字符串用作错误消息，而不是默认错误消息。显然，“:”和“;”相互排斥。
*/

extern PyObject *Py_BuildValue(char *format, ...);
/*
Py_BuildValue()函数的作用和PyArg_ParseTuple()的作用相反，它是将C类型的数据结构转换成Python对象，该函数的原型:

该函数可以和PyArg_ParseTuple()函数一样识别一系列的格式串，但是输入参数只能是值，而不能是指针。它返回一个Python对象。
和PyArg_ParseTuple()不同的一点是PyArg_ParseTuple()函数它的第一个参数为元组，Py_BuildValue()则不一定会生成一个元组。
它生成一个元组仅仅当格式串包含两个或者多个格式单元，如果格式串为空，返回NONE。

在下面的描述中，括号中的项是格式单元返回的Python对象类型，方括号中的项为传递的C的值的类型。
"s" (string) [char *] ：将C字符串转换成Python对象，如果C字符串为空，返回NONE。
"s#" (string) [char *, int] :将C字符串和它的长度转换成Python对象，如果C字符串为空指针，长度忽略，返回NONE。
"z" (string or None) [char *] :作用同"s"。
"z#" (string or None) [char *, int] :作用同"s#"。
"i" (integer) [int] :将一个C类型的int转换成Python int对象。
"b" (integer) [char] :作用同"i"。
"h" (integer) [short int] ：作用同"i"。
"l" (integer) [long int] :将C类型的long转换成Pyhon中的int对象。
"c" (string of length 1) [char] ：将C类型的char转换成长度为1的Python字符串对象。
"d" (float) [double] :将C类型的double转换成python中的浮点型对象。
"f" (float) [float] :作用同"d"。
"O&" (object) [converter, anything] ：将任何数据类型通过转换函数转换成Python对象，这些数据作为转换函数的参数被调用并且返回一个新的Python对象，如果发生错误返回NULL。
"(items)" (tuple) [matching-items] ：将一系列的C值转换成Python元组。
"[items]" (list) [matching-items] ：将一系列的C值转换成Python列表。
"{items}" (dictionary) [matching-items] ：将一系类的C值转换成Python的字典，每一对连续的C值将转换成一个键值对。
*/