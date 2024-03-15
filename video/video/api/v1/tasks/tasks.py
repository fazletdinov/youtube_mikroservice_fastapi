import base64

from celery import Celery

from video.core.config import settings

celery = Celery(
    "tasks",
    backend=settings.redis.backend_url,
    broker=settings.rabbitmq.broker_url,
)
celery.conf.broker_connection_retry_on_startup = True


# loop = asyncio.get_event_loop()


@celery.task
def write_video(file_name: str, video_base64: str):
    file = base64.b64decode(video_base64)
    with open(file_name, "wb") as buffer:
        buffer.write(file)
    return {"status": True}


@celery.task
def write_image(file_name: str, image_base64: str):
    image = base64.b64decode(image_base64)
    with open(file_name, "wb") as file:
        file.write(image)
    return {"status": True}
