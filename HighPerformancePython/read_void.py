# coding:utf-8
from struct import unpack, pack
# 内存数据打包与解包
'''
Format	C Type	      Python	字节数
x	    pad byte	  no value	1
c	    char	      string of length 1	1
b	    signed char	  integer	1
B	    unsigned char integer	1
?	    _Bool	      bool	1
h	    short	      integer	2
H	    unsigned short	integer	2
i	    int	          integer	4
I	    unsigned int  integer or long	4
l	    long	      integer	4
L	    unsigned long	long	4
q	    long long	  long	8
Q	    unsigned long long	long	8
f	    float	      float	4
d	    double	      float	8
s	    char[]	      string	1
p	    char[]	      string	1
P	    void *	      long
'''

'''

Character	Byte order	        Size and alignment
@	        native	            native    凑够4个字节
=	        native	            standard  按原字节数
<	        little-endian	    standard  按原字节数
>	        big-endian	        standard  按原字节数
!	        network (big-endian)	standard 按原字节数
'''
code = b"600000"
market = b"\1"
buy_price = 1100
buy_vol = 213
sell_price = 1098
sell_vol = 104
format_str = "@7s1siiii"            # 打包格式
bytes = pack(format_str, code, market, buy_price, buy_vol, sell_price, sell_vol)
order_book = unpack("@7s1siiii", bytes)
m = int.from_bytes(order_book[1], byteorder='big', signed=False)
print("market:{:d}".format(m))
print(order_book)