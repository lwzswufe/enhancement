import redis   
# 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库

# host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
r = redis.Redis(host='localhost', port=6379, decode_responses=True)   
# key是"foo" value是"bar" 将键值对存入redis缓存
# 设置键name对应的值
# set(name, value, ex=None, px=None, nx=False, xx=False)
# 在Redis中设置值，默认，不存在则创建，存在则修改
# 参数：
# ex，过期时间（秒）
# px，过期时间（毫秒）
# nx，如果设置为True，则只有name不存在时，当前set操作才执行
# xx，如果设置为True，则只有name存在时，当前set操作才执行
r.set("设置:", 'name', 'junxi')  
print(r['name'])
# 取出键name对应的值
print("取出:", r.get('name'))  
print(type(r.get('name')))
# 修改键name对应的值
old_name = r.getset("name", "haha")
print("將 name 从 {} 修改为 {}".format(old_name, r.get('name')))
# 刪除键name对应的值
r.delete('name')
print("刪除:", r.get('name'))

# 批量设置值
# mset(*args, **kwargs)
r.mset({'k1': 'v1', 'k2': 831}) 
print("批量设置值:", r.mget("k1", "k2"))   # 一次取出多个键对应的值
print("批量设置值:", r.mget("k1"))

# 批量获取
# mget(keys, *args)
print("批量获取值:", r.mget('k1', 'k2'))
print("批量获取值:", r.mget(['k1', 'k2']))
print("批量获取值:", r.mget("fruit", "fruit1", "fruit2", "k1", "k2"))  # 将目前redis缓存中的键对应的值批量取出来
