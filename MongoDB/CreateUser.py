from pymongo import MongoClient


'''
https://www.mongodb.com/docs/manual/reference/command/
'''


def login(server: str, port: int, user: str = "", pwd: str = "") -> MongoClient:
    '''
    登陆数据库 返回句柄
    :param server: 数据库服务器ip
    :param port: 数据库服务器端口号
    :param user: 用户名
    :param pwd: 密码
    :return:
    '''
    if user == "":
        uri = 'mongodb://{}:{}'.format(server, port)
    else:
        uri = 'mongodb://{}:{}@{}:{}'.format(user, pwd, server, port)
    client = MongoClient(uri)
    return client


def show_user(client: MongoClient):
    '''
    显示当前用户
    :param client: 数据库接口句柄
    :return:
    '''
    basename = 'admin'
    db = client.get_database(basename)   # 创建base
    # table = db.get_collection(tablename)  # 获取表
    # cursor = table.find()
    r = db.command({"usersInfo": 1})
    if len(r) > 0 and "users" in r.keys():
        return r["users"]
    return None


def add_user(client: MongoClient, name: str, password: str, role: str):
    '''
    插入用户
    :param role: 角色-权限
    :param name: 用户名
    :param password: 密码
    :param client: 数据库接口句柄
    :return:
    '''
    command = {
        "createUser": name,
        "pwd": password,
        "roles": [
            {"role": role, "db": "admin"},
                ]
        }
    basename = 'admin'
    db = client.get_database(basename)
    r = db.command(command)
    print(r)


def del_user(client: MongoClient, user_name):
    '''
    删除指定用户
    :param client: 数据库接口句柄
    :param user_name: 待删除的用户名
    :return:
    '''
    basename = 'admin'
    db = client.get_database(basename)
    command = {
        "dropUser": user_name}
    r = db.command(command)
    print(r)


def main():
    client = login("localhost", 27017)
    users = show_user(client)
    print(users)
    add_user(client, "reader", "123456", "readAnyDatabase")
    users = show_user(client)
    print(users)


if __name__ == "__main__":
    main()
