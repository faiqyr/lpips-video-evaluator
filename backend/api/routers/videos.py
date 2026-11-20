import os
import shutil
import uuid
import zipfile
import io
import tempfile
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from api.deps import get_db
from models.all_models import Video, EvaluationStatus
from schemas.all_schemas import VideoResponse
from core.config import settings
from services.video_service import extract_all_frames

router = APIRouter()


def process_video_background(video_id: int, filepath: str, frame_folder: str):
    """Extract frames from video in background thread."""
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        def progress_callback(progress_val: float):
            v = db.query(Video).filter(Video.id == video_id).first()
            if v:
                v.progress = round(progress_val, 2)
                db.commit()

        total_frames, fps = extract_all_frames(filepath, frame_folder, progress_callback=progress_callback)
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.total_frames = total_frames
            video.fps = fps
            video.progress = 100.0
            video.status = EvaluationStatus.completed
            db.commit()
    except Exception as e:
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.status = EvaluationStatus.failed
            db.commit()
        print(f"Frame extraction failed for video {video_id}: {e}")
    finally:
        db.close()


@router.get("/", response_model=List[VideoResponse])
def list_videos(db: Session = Depends(get_db)):
    """List all uploaded videos."""
    videos = db.query(Video).order_by(Video.created_at.desc()).all()
    return videos


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get a single video by ID."""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.post("/upload", response_model=VideoResponse)
def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a single MP4 video and start frame extraction."""
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 files are supported")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.FRAME_DIR, exist_ok=True)

    unique_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{unique_id}{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, saved_filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    frame_folder = os.path.join(settings.FRAME_DIR, unique_id)

    video = Video(
        filename=file.filename,
        filepath=filepath,
        frame_folder=frame_folder,
        status=EvaluationStatus.processing
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    background_tasks.add_task(process_video_background, video.id, filepath, frame_folder)

    return video


@router.get("/{video_id}/download-frames")
def download_frames(video_id: int, db: Session = Depends(get_db)):
    """Download extracted frames as a ZIP file."""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.status != EvaluationStatus.completed:
        raise HTTPException(status_code=400, detail="Frame extraction not completed yet")

    if not video.frame_folder or not os.path.exists(video.frame_folder):
        raise HTTPException(status_code=404, detail="Frame folder not found")

    # Create ZIP in a temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".zip")
    with os.fdopen(fd, 'wb') as f:
        with zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(video.frame_folder):
                for fname in sorted(files):
                    file_path = os.path.join(root, fname)
                    zf.write(file_path, fname)

    filename_base = os.path.splitext(video.filename)[0]
    from starlette.background import BackgroundTask
    return FileResponse(
        path=temp_path,
        media_type="application/zip",
        filename=f"{filename_base}_frames.zip",
        background=BackgroundTask(os.remove, temp_path)
    )


@router.delete("/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    """Delete a video and its associated files."""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Clean up files
    if video.filepath and os.path.exists(video.filepath):
        os.remove(video.filepath)
    if video.frame_folder and os.path.exists(video.frame_folder):
        shutil.rmtree(video.frame_folder)

    db.delete(video)
    db.commit()
    return {"ok": True}
