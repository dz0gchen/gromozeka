import random
from aiohttp import web


async def handler(request: web.Request) -> web.Response:
    rand = random.randint(0, 9)
    status = 200
    if rand % 2 == 0:
        status = 201
    elif rand % 3 == 0:
        status = 404
    return web.json_response(data={"boooms": "baaams"}, status=status, content_type='application/json', headers={})


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.get("/", handler)])
    return app

#run server: gunicorn server:init_app --worker-class aiohttp.GunicornWebWorker
