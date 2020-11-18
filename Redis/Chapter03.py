import redis 

# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
r = redis.Redis(host='localhost', port=6379, decode_responses=True) 


# 1. Sadd 命令将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略。
# 假如集合 key 不存在，则创建一个只包含添加的元素作成员的集合。当集合 key 不是集合类型时，返回一个错误。
# 2.Scard 命令返回集合中元素的数量。集合的数量。 当集合 key 不存在时，返回 0 。
# 3.Sdiff 命令返回给定集合之间的差集。不存在的集合 key 将视为空集。
# 4.Sdiffstore 命令将给定集合之间的差集存储在指定的集合中。如果指定的集合 key 已存在，则会被覆盖。
# 5.Sinter 命令返回给定所有给定集合的交集。 不存在的集合 key 被视为空集。 当给定集合当中有一个空集时，结果也为空集(根据集合运算定律)。
# 6.Sinterstore 命令将给定集合之间的交集存储在指定的集合中。如果指定的集合已经存在，则将其覆盖。
# 7.Sismember 命令判断成员元素是否是集合的成员。
# 8.Smembers 命令返回集合中的所有的成员。 不存在的集合 key 被视为空集合。
# 9.Smove 命令将指定成员 member 元素从 source 集合移动到 destination 集合。
# 10.Spop 命令用于移除并返回集合中的一个随机元素。
# 11.Srandmember 命令用于返回集合中的一个随机元素。
# 12.Srem 命令用于移除集合中的一个或多个成员元素，不存在的成员元素会被忽略。
# 13.Sunion 命令返回给定集合的并集。不存在的集合 key 被视为空集。
# 14.Sunionstore 命令将给定集合的并集存储在指定的集合 destination 中。
# 15.Sscan 命令用于迭代集合键中的元素。 SSCAN KEY [MATCH pattern] [COUNT count]
print("集合 1 添加元素 1：", r.sadd("1",1))       # 输出的结果是1
print("显示集合 1元素个数:", r.scard("1"))        # 输出的结果是1
print("集合 1 添加元素 2：", r.sadd("1",2))       # 输出的结果是1
print("集合 1 添加元素 2：", r.sadd("1",2))       # 因为2已经存在，不能再次田间，所以输出的结果是0
print("集合 1 添加元素 3 4：", r.sadd("1",3,4))   # 输出的结果是2
print("显示集合 1 元素个数:", r.scard("1"))                    # 输出的结果是1
print("显示集合 1：", r.smembers("1"))         #输出的结果是set(['1', '3', '2', '4'])
print("判断元素 7 是否是集合 1 的成员：", r.sismember("1", 7) )
print("判断元素 3 是否是集合 1 的成员：", r.sismember("1", 3) )

r.sadd("2",2,3,5,7)   #输出的结果是1
print("显示集合 2：", r.smembers("2"))   

print("显示集合 1 2 差集：", r.sdiff(1, 2))
print("显示集合 1 2 交集：", r.sinter(1, 2))
print("显示集合 1 2 并集：", r.sunion(1, 2))

print("把集合 1中的 元素4 移动到 集合 2中去：", r.smove(1, 2, 4))
print("显示集合 1：", r.smembers("1"))
print("显示集合 2：", r.smembers("2"))  

print("从集合2 随机移除元素：", r.spop("2"))              
print("显示集合 2：", r.smembers("2"))  

print("从集合2 随机放回抽样返回元素：", r.srandmember(2, -3))
print("从集合2 随机不放回抽样返回元素：", r.srandmember(2, 2)) 

print("从集合2 删除元素 8:", r.srem("2",8))  
print("从集合2 删除元素 7:", r.srem("2",7))  
print("显示集合 2：", r.smembers("2"))   

for i in range(20):
    r.sadd(2, i)
print(r.sscan(2, cursor=0, match="1*", count=1))
print(r.sscan(2, cursor=1, count=1))

r.unlink("1")                             # 删除集合 1
r.unlink("2")                             # 删除集合 2
print("清空集合元素 1:",r.smembers("1"))
print("清空集合元素 2:",r.smembers("2"))
