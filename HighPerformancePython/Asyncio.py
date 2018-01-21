# author='lwz'
# coding:utf-8

import asyncio
import random
import string
import time


def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def chunked_http_client(num_chunks):
    semaphore = asyncio.Semaphore(num_chunks)

    @asyncio.coroutine
    # 调用他们中的任意一个,实际上并未立即运行,而是返回一个协程对象,然后将其传递到 Eventloop 中,之后再执行。
    # 判断一个函数是不是协程, asyncio 提供了 asyncio.iscoroutinefunction(func) 方法
    def http_get(url):
        nonlocal semaphore
        with (yield from semaphore):
            # yield from 表达式允许一个生成器代理另一个生成器, 这样就允许生成器被替换为另一个生成器, 子生成器允许返回值
            # yield from的前世今生都在 这个PEP里面，总之大意是原本的yield语句只能将CPU控制权 还给直接调用者，当你想要将
            # 一个generator或者coroutine里带有 yield语句的逻辑重构到另一个generator（原文是subgenerator） 里的时候，会
            # 非常麻烦，因为外面的generator要负责为里面的 generator做消息传递；所以某人有个想法是让python把消息传递
            # 封装起来，使其对程序猿透明，于是就有了yield from。
            # Python下 的coroutine将“消息传递”和“调度”这两种操作绑在一个yield 上——即便有了yield from

            # response = yield from aiohttp.request('GET', url)
            # body = yield from response.content.read()
            # yield from response.wait_for_close()
            body = get_body(url)
        return body
    return http_get


def get_body(url):
    time.sleep(0.001)
    return 1


def run_experiment(base_url, num_iter=500):
    urls = generate_urls(base_url, num_iter)
    http_client = chunked_http_client(100)
    tasks = [http_client(url) for url in urls]
    responses_sum = 0
    for future in asyncio.as_completed(tasks):
        data = yield from future
        responses_sum += data
    return responses_sum

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    delay = 25
    num_iter = 500

    start = time.time()
    result = loop.run_until_complete(
        run_experiment(
            "http://127.0.0.1:8080/add?name=asyncio&delay={}&".format(delay),
            num_iter))
    end = time.time()
    print("{} times used {:.4f}s".format(result, end - start))