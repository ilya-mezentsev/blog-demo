import prometheus_client  # type: ignore
from aiohttp import web

from .middleware import prom_middleware


__all__ = [
    'metrics',
    'setup_metrics',
]


async def metrics(_: web.Request) -> web.Response:
    resp = web.Response(
        body=prometheus_client.generate_latest(),
        content_type='application/json',
    )

    return resp


def setup_metrics(app: web.Application, app_name: str) -> None:

    app['REQUEST_TIME'] = prometheus_client.Histogram(
        name='request_processing_seconds',
        documentation='Time of request processing (in seconds)',
        labelnames=[
            'app_name',
            'endpoint',
        ],
    )

    app.middlewares.insert(0, prom_middleware(app_name))
    app.router.add_get("/metrics", metrics)
