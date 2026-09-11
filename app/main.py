from uuid import uuid4
from fastapi import FastAPI, Request
from app.config import settings
from app.routers.products import router as products_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Microservicio de catálogo de OrderFlow.",
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


app.include_router(products_router, prefix="/api/v1")
