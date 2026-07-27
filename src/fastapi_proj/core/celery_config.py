from celery import Celery

from fastapi_proj.core.settings import settings

celery_app = Celery(
    main="fastapi_proj",
    broker=settings.redis_settings.redis_url,
    backend=settings.redis_settings.redis_url,
)

celery_app.autodiscover_tasks(packages=["fastapi_proj.apps"])
