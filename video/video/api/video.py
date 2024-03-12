from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Header, Request, Response, UploadFile
from fastapi.templating import Jinja2Templates

from video.services.video import VideoService, get_service_video

video_router = APIRouter(tags=["Video"])
templates = Jinja2Templates(directory="src/templates")
CHUNK_SIZE = 1024 * 1024


@video_router.get("/{video_id}")
async def read_root(video_id: int, request: Request):
    return templates.TemplateResponse(
        "index.html", context={"request": request, "path": video_id}
    )


@video_router.post("/")
async def create_video(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    file: UploadFile,
    image: UploadFile,
    video_service: VideoService = Depends(get_service_video),
):
    await video_service.create_video(title, description, file, image)
    return {"status": "Видео загружается"}


@video_router.get("/video/{video_id}")
async def video_endpoint(
    video_id: int,
    range: str = Header(None),
    video_service: VideoService = Depends(get_service_video),
):
    video_path = await video_service.get_video(video_id)
    path = Path(video_path.file)
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(path.stat().st_size)
        headers = {
            "Content-Range": f"bytes {str(start)}-{str(end)}/{filesize}",
            "Accept-Ranges": "bytes",
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
