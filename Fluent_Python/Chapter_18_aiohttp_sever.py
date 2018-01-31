# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import asyncio
from aiohttp import web
import sys


'''
如需要网络上其他机器访问需要设置本机地址为本机局域网IP
cmd命令 ipconfig 查询本机IP
然后外网机器可以通过本机外网IP访问
'''
TODOS = dict(zip([0, 1, 2, 3], ["zero", "first", "second", "third"]))


@asyncio.coroutine
def get_dict(request):
    print("url: ", request.path)
    data = yield from request.json()
    print(data)

    # return web.json_response("post success")
    return web.Response(text="post success")


@asyncio.coroutine
def get_str(request):
    print("url: ", request.path)
    data = yield from request.text()
    print(data)

    return web.Response(text="put success")


def querys(request):
    print("url: ", request.path)
    return web.json_response(TODOS)


def query_one(request):
    print("url: ", request.path)
    idx = int(request.match_info['id'])

    if idx >= len(TODOS):
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response({'id': TODOS[idx]})


@asyncio.coroutine
def init(loop, address, port):
    app = web.Application(loop=loop)  # 设置路由
    # app.router.add_route('GET', '/', home)

    app.router.add_get('/get/', querys, name='all_todos')  # 注册get方法
    app.router.add_get('/get/{id:\d+}', query_one, name='one_todo')  # 正则表达式
    app.router.add_post('/post/', get_dict, name='create_todo')  # 注册post方法
    app.router.add_put('/put/', get_str, name='creates_todo')   # 注册put方法

    handler = app.make_handler()
    server = yield from loop.create_server(handler,
    address, port)
    return server.sockets[0].getsockname()


def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
        print('Server shutting down.')
        loop.close()


if __name__ == '__main__':
    main(*sys.argv[1:])