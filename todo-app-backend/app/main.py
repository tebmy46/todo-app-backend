import logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.category import router as category_router
from app.api.routers.task import router as task_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()

settings = get_settings()
app = FastAPI()
app.state.request_count = 0
logger = logging.getLogger("app.middleware")

app.include_router(router=task_router)
app.include_router(router=category_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-Number"],
)


@app.middleware("http")
async def log_requests(
    request: Request,
    call_next,
) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.middleware("http")
async def count_requests(
    request: Request,
    call_next,
) -> Response:
    app.state.request_count += 1
    request_number = app.state.request_count
    response: Response = await call_next(request)
    response.headers["X-Request-Number"] = str(request_number)

    return response
