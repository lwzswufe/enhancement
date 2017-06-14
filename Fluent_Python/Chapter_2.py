# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import sys
from collections import namedtuple


symbols = "%&*$#@"
codes = [ord(symbol) for symbol in symbols]
print(codes)


# input("Press Enter to continue: ")
colors = ['blacks', 'white', 'blue']
sizes = ['S', 'M', 'L']
T_shirts = [(color, size) for color in colors for size in sizes]
print(T_shirts)                   # 生成元组
print(type(T_shirts[0]))          # tuple
print(dict(T_shirts))
print(dict(zip(colors, sizes)))   # 由key和 values生成字典

a, *rest, b = range(7)    # *rest 接受多余的参数


metro_areas = [('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),  #
			   ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
			   ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
			   ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
               ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))  ]
print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:  # 嵌套元组拆包
	if longitude <= 0:  # 经度
		print(fmt.format(name, latitude, longitude))


City = namedtuple('City', 'name country population coordinates')  # 具名元组
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))      # 赋值
print(tokyo)
print(tokyo.coordinates)
City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))
print(tokyo.population)
print(tokyo.coordinates)
print(tokyo[1])

