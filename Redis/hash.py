import redis 

# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
r = redis.Redis(host='localhost', port=6379, decode_responses=True) 

'''
1. Hset 命令用于为哈希表中的字段赋值 。如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。如果字段已经存在于哈希表中，旧值将被覆盖。
如果字段是哈希表中的一个新建字段，并且值设置成功，返回 1 。 如果哈希表中域字段已经存在且旧值已被新值覆盖，返回 0 。
2.Hdel 命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。
3.Hexists  命令用于查看哈希表的指定字段是否存在。如果哈希表含有给定字段，返回 True 。 如果哈希表不含有给定字段，或 key 不存在，返回False 。
4.Hget 命令用于返回哈希表中指定字段的值。返回给定字段的值。如果给定的字段或 key 不存在时，返回 None 。
5.Hgetall 命令用于返回哈希表中，所有的字段和值。在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，所以返回值的长度是哈希表大小的两倍。
6.Hincrby 命令用于为哈希表中的字段值加上指定增量值。
增量也可以为负数，相当于对指定字段进行减法操作。
如果哈希表的 key 不存在，一个新的哈希表被创建并执行 HINCRBY 命令。
如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0 。
对一个储存字符串值的字段执行 HINCRBY 命令将造成一个错误。
7. Hincrbyfloat 命令用于为哈希表中的字段值加上指定浮点数增量值。
如果指定的字段不存在，那么在执行命令前，字段的值被初始化为 0 。
8.Hkeys 命令用于获取哈希表中的所有字段名。包含哈希表中所有字段的列表。 当 key 不存在时，返回一个空列表。
9.Hlen 命令用于获取哈希表中字段的数量。哈希表中字段的数量。 当 key 不存在时，返回 0 。
10. Hmget 命令用于返回哈希表中，一个或多个给定字段的值。如果指定的字段不存在于哈希表，那么返回一个 nil 值。
一个包含多个给定字段关联值的表，表值的排列顺序和指定字段的请求顺序一样。
11. Hmset 命令用于同时将多个 field-value (字段-值)对设置到哈希表中。
此命令会覆盖哈希表中已存在的字段。
如果哈希表不存在，会创建一个空哈希表，并执行 HMSET 操作。
12. Hsetnx 命令用于为哈希表中不存在的的字段赋值 。
如果哈希表不存在，一个新的哈希表被创建并进行 HSET 操作。
如果字段已经存在于哈希表中，操作无效。
如果 key 不存在，一个新哈希表被创建并执行 HSETNX 命令。
设置成功，返回 1 。 如果给定字段已经存在且没有操作被执行，返回 0 。
13 Hvals 命令返回哈希表所有字段的值。一个包含哈希表中所有值的表。 当 key 不存在时，返回一个空表。
'''



print("设置哈希表1 键key1 对应的值为 value:", r.hset(name="1",key="key1",value="value"))  #返回的结果是 1
print("获取哈希表1 键key1 对应的值:", r.hget(name="1",key="key1"))    #返回的结果是 value
print("设置哈希表1 键key1 对应的值为 hello world:",  r.hset(name="1",key="key1",value="hello world"))  #返回的结果是 0,原因是哈希表中域字段已经存在且旧值已被新值覆盖
print("获取哈希表1 键key1 对应的值:", r.hget(name="1",key="key1"))    #返回的结果是 hello world
print("删除哈希表1:", r.delete("name"))
print("获取哈希表1 键key1 对应的值:", r.hget(name="1",key="key1"))  

print("查看哈希表的指定字段key 1是否存在:", r.hexists(name="1",key="key1"))   # 返回的结果是 False
print("设置哈希表1 键key1 对应的值为 value:", r.hset(name="1",key="key1",value="value"))
print("查看哈希表的指定字段key 1是否存在:", r.hexists(name="1",key="key1"))   
print("获取哈希表1 键key1 对应的值:", r.hget(name="1",key="key1"))  

print("设置哈希表2 键1 对应的值为1:", r.hset(name="2", key="1", value="1"))  # 返回的结果是 1
print("设置哈希表2 键3 对应的值为2:", r.hset(name="2", key="3", value="2"))  # 返回的结果是 1
print("设置哈希表2 键2 对应的值为3:", r.hset(name="2", key="2", value="3"))  # 返回的结果是 1
print("设置哈希表2 键2 对应的值为4:", r.hset(name="2", key="2", value="4"))  # 返回的结果是 0   如果不知道为什么返回的结果是0，请看hset

print("获取哈希表1 所有对应的值:", r.hgetall("1"))    # 返回的结果是 {'1': '1', '3': '2', '2': '4'}  主意返回的数据格式
print("获取哈希表2 所有对应的值:", r.hgetall("2"))   # 因为字典名2 不存在，所以返回的结果是 {}

print("获取哈希表2 键1 对应的值:", r.hget(name="1",key="key1"))  
print("使得哈希表2 键1 对应的值增加1.2:", r.hincrbyfloat(name="2",key="1",amount="1.2"))  # 返回的结果是 2.2
print("获取哈希表2 键1 对应的值:", r.hget(name="1",key="key1"))  

print("哈希表2 中的所有字段名:", r.hkeys(2))
print("哈希表2 中的所有字段值:", r.hvals(2))
print("哈希表2 中的字段数量:", r.hvals(2))

print("尝试设置哈希表1 键1 对应的值为1: 成功", r.hsetnx(name="1",key="1",value="1"))   # 返回的结果是 1
print("尝试设置哈希表1 键1 对应的值为2: 失败 键已存在", r.hsetnx(name="1",key="1",value="2"))   # 返回的结果是 0

r.unlink("1")                             # 删除哈希 1
r.unlink("2")                             # 删除哈希 2