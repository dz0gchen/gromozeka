import asyncio
import argparse
from collections import Counter
from datetime import datetime
import time

import aiohttp
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

statistics_store, response_store = list(), list()

async def _request(rps: int, url: str, duration: int = 10):
    loop = asyncio.get_running_loop()
    # when making requests to real addresses, the default resolver is used
    # https://github.com/aio-libs/aiohttp/blob/master/aiohttp/resolver.py#L118
    # ThreadedResolver spawns additional threads, the limit from the parameter --users is violated
    resolver = aiohttp.resolver.AsyncResolver(loop=loop)
    connector = aiohttp.TCPConnector(loop=loop, ssl=False, resolver=resolver)
    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:
        now = datetime.now()
        while (datetime.now()-now).seconds <= duration:
                start = time.perf_counter()
                async with session.get(url) as response:
                    await response.text()
                delta = time.perf_counter() - start
                await asyncio.sleep(1/rps)
                # these are thread-safe operations without the need for locks,
                # as an increased price we introduce an additional list
                # instead of adding to Counter at this place
                statistics_store.append(delta)
                response_store.append(response.status)


def url(arg: str):
    _url = urlparse(arg)
    if all((_url.scheme, _url.netloc)):
        return arg
    raise ValueError


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gromozeka is load testing utility')
    parser.add_argument('--rps', type=int, choices=range(1, 1000), required=True,
                        help='limiting the number of requests per second per user')
    parser.add_argument('--users', type=int, choices=range(1, 500), required=True,
                        help='number of users sending requests in parallel')
    parser.add_argument("--url", type=url, required=True, help='address of the server or service being tested')
    parser.add_argument('--duration', type=int, choices=range(1, 3600), help='test duration in seconds')

    args = parser.parse_args()

    r_args = [args.rps, args.url]
    if args.duration is not None:
        r_args.append(args.duration)

    with ThreadPoolExecutor(args.users) as executor:
        [executor.submit(asyncio.run, _request(*r_args)) for _ in range(args.users)]

    print('== max response time')
    print(max(statistics_store))
    print('== average response time')
    print(sum(statistics_store)/len(statistics_store))
    print('== number of response')
    print(len(response_store))
    print('== number of response codes')
    for c, v in Counter(response_store).items():
        print('{0} : {1}'.format(c, v))
