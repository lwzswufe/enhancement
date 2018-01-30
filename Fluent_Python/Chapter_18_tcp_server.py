# author='lwz'
# coding:utf-8
# !/usr/bin/env python3
import sys
import asyncio


@asyncio.coroutine
def handle_queries(reader, writer):
    writer.write(b"hello")
    while True:
        # writer.write(PROMPT)  # can't yield from!
        try:
            yield from writer.drain()  # must yield from!
            data = yield from reader.readline()
        except ConnectionResetError:
            print("远程主机强迫关闭了一个现有的连接。....等待连接")
            # 如果连接方程序断开 会触发ConnectionResetError
            # 这里需要退出循环防止循环报错
            break

        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'

        if len(data) == 0:
            print("远程主机发送空数据...连接关闭")
            break

        client = writer.get_extra_info('peername')
        print('Received from {}: {!r}'.format(client, query))
        if query:
            results = sum([ord(q) for q in query])
            context = "the sum ords is {}".format(results)
            writer.write(bytes(context, encoding="utf-8"))
            print("Send:", context)

            try:
                yield from writer.drain()
            except ConnectionResetError:
                print("远程主机强迫关闭了一个现有的连接。....等待连接")
                # 这里需要退出循环防止循环报错
                break

    print('Close the client socket')
    writer.close()


def main(address='127.0.0.1', port=2323):
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, address, port,
    loop=loop)
    server = loop.run_until_complete(server_coro)
    host = server.sockets[0].getsockname()
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))

    try:
        loop.run_forever()
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
    print('Server shutting down.')

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main(*sys.argv[1:])
    main("rook")
