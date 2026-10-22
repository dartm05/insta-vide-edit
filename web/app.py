"""
FastAPI Web Application for Instagram Video Editor
"""
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import aiofiles

# Add parent directory to path for imports
import sys
video_agent_path = Path(__file__).parent.parent / "video_agent"
sys.path.insert(0, str(video_agent_path))

from src.analysis.style_analyzer import learn_from_video, apply_style_to_video
from src.models.editing_style import EditingStyle, get_preset_style, list_preset_styles
from src.core.pipeline import quick_convert

# Setup loguru
from loguru import logger
logger.add(sys.stderr, level="INFO")

# Initialize FastAPI app
app = FastAPI(
    title="Instagram Video Editor",
    description="AI-powered video editing with style transfer",
    version="1.0.0"
)

# Setup directories
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
STYLES_DIR = BASE_DIR / "styles"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

for directory in [UPLOAD_DIR, RESULTS_DIR, STYLES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# In-memory job storage (use Redis in production)
jobs = {}


class JobStatus:
    """Job status tracker."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def create_job(job_type: str, **kwargs) -> str:
    """Create a new job."""
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "id": job_id,
        "type": job_type,
        "status": JobStatus.PENDING,
        "created_at": datetime.now().isoformat(),
        "progress": 0,
        "result": None,
        "error": None,
        **kwargs
    }
    return job_id


def update_job(job_id: str, **kwargs):
    """Update job status."""
    if job_id in jobs:
        jobs[job_id].update(kwargs)


async def save_upload_file(upload_file: UploadFile, destination: Path) -> Path:
    """Save uploaded file to disk."""
    async with aiofiles.open(destination, 'wb') as out_file:
        content = await upload_file.read()
        await out_file.write(content)
    return destination


def process_video_conversion(
    job_id: str,
    input_path: Path,
    format_name: str,
    output_dir: Path
):
    """Background task: Convert video to Instagram format."""
    try:
        update_job(job_id, status=JobStatus.PROCESSING, progress=10)

        logger.info(f"Job {job_id}: Converting {input_path.name} to {format_name}")

        # Convert video
        from src.core.video_output import VideoOutput
        output_path = VideoOutput.export_for_format(
            input_path,
            format_name,
            output_dir,
        )

        update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            result=str(output_path.name)
        )

        logger.info(f"Job {job_id}: Completed - {output_path}")

    except Exception as e:
        logger.error(f"Job {job_id}: Failed - {e}")
        update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e)
        )


def process_style_transfer(
    job_id: str,
    reference_path: Path,
    input_path: Path,
    format_name: str,
    output_dir: Path,
    style_name: Optional[str] = None
):
    """Background task: Apply style transfer."""
    try:
        update_job(job_id, status=JobStatus.PROCESSING, progress=10)

        logger.info(f"Job {job_id}: Learning style from {reference_path.name}")

        # Learn style from reference
        update_job(job_id, progress=30)
        style = learn_from_video(
            reference_path,
            style_name or f"Style-{job_id[:8]}"
        )

        # Save style
        style_path = STYLES_DIR / f"style_{job_id}.json"
        style.save(style_path)

        logger.info(f"Job {job_id}: Applying style to {input_path.name}")

        # Apply style
        update_job(job_id, progress=60)
        output_path = apply_style_to_video(
            input_path,
            style,
            format_name
        )

        # Move to results directory
        final_output = output_dir / output_path.name
        shutil.move(str(output_path), str(final_output))

        update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            result=str(final_output.name),
            style_file=str(style_path.name)
        )

        logger.info(f"Job {job_id}: Completed - {final_output}")

    except Exception as e:
        logger.error(f"Job {job_id}: Failed - {e}")
        update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e)
        )


def process_preset_style(
    job_id: str,
    input_path: Path,
    preset_name: str,
    format_name: str,
    output_dir: Path
):
    """Background task: Apply preset style."""
    try:
        update_job(job_id, status=JobStatus.PROCESSING, progress=20)

        logger.info(f"Job {job_id}: Applying preset '{preset_name}' to {input_path.name}")

        # Get preset style
        style = get_preset_style(preset_name)

        # Apply style
        update_job(job_id, progress=60)
        output_path = apply_style_to_video(
            input_path,
            style,
            format_name
        )

        # Move to results directory
        final_output = output_dir / output_path.name
        shutil.move(str(output_path), str(final_output))

        update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            result=str(final_output.name)
        )

        logger.info(f"Job {job_id}: Completed - {final_output}")

    except Exception as e:
        logger.error(f"Job {job_id}: Failed - {e}")
        update_job(
            job_id,
            status=JobStatus.FAILED,
            error=str(e)
        )


# API Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    preset_styles = []
    for style_name in list_preset_styles():
        style = get_preset_style(style_name)
        preset_styles.append({
            'id': style_name,
            'name': style.name,
            'description': style.description
        })

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "preset_styles": preset_styles
        }
    )


@app.post("/api/convert")
async def convert_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    format: str = Form(...),
):
    """Convert video to Instagram format."""

    # Validate format
    valid_formats = ['stories', 'reels', 'feed_square', 'feed_portrait', 'feed_landscape']
    if format not in valid_formats:
        raise HTTPException(400, f"Invalid format. Must be one of: {valid_formats}")

    # Save uploaded file
    file_extension = Path(video.filename).suffix
    upload_path = UPLOAD_DIR / f"{uuid.uuid4()}{file_extension}"
    await save_upload_file(video, upload_path)

    # Create job
    job_id = create_job(
        job_type="convert",
        input_file=str(upload_path.name),
        format=format
    )

    # Start background processing
    background_tasks.add_task(
        process_video_conversion,
        job_id,
        upload_path,
        format,
        RESULTS_DIR
    )

    return {"job_id": job_id, "status": "processing"}


@app.post("/api/style-transfer")
async def style_transfer(
    background_tasks: BackgroundTasks,
    reference_video: UploadFile = File(...),
    input_video: UploadFile = File(...),
    format: str = Form(...),
    style_name: Optional[str] = Form(None),
):
    """Apply style transfer from reference video."""

    # Validate format
    valid_formats = ['stories', 'reels', 'feed_square', 'feed_portrait', 'feed_landscape']
    if format not in valid_formats:
        raise HTTPException(400, f"Invalid format. Must be one of: {valid_formats}")

    # Save uploaded files
    ref_extension = Path(reference_video.filename).suffix
    ref_path = UPLOAD_DIR / f"ref_{uuid.uuid4()}{ref_extension}"
    await save_upload_file(reference_video, ref_path)

    input_extension = Path(input_video.filename).suffix
    input_path = UPLOAD_DIR / f"input_{uuid.uuid4()}{input_extension}"
    await save_upload_file(input_video, input_path)

    # Create job
    job_id = create_job(
        job_type="style_transfer",
        reference_file=str(ref_path.name),
        input_file=str(input_path.name),
        format=format,
        style_name=style_name
    )

    # Start background processing
    background_tasks.add_task(
        process_style_transfer,
        job_id,
        ref_path,
        input_path,
        format,
        RESULTS_DIR,
        style_name
    )

    return {"job_id": job_id, "status": "processing"}


@app.post("/api/preset-style")
async def apply_preset_style(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    preset: str = Form(...),
    format: str = Form(...),
):
    """Apply a preset editing style."""

    # Validate preset
    valid_presets = list_preset_styles()
    if preset not in valid_presets:
        raise HTTPException(400, f"Invalid preset. Must be one of: {valid_presets}")

    # Validate format
    valid_formats = ['stories', 'reels', 'feed_square', 'feed_portrait', 'feed_landscape']
    if format not in valid_formats:
        raise HTTPException(400, f"Invalid format. Must be one of: {valid_formats}")

    # Save uploaded file
    file_extension = Path(video.filename).suffix
    upload_path = UPLOAD_DIR / f"{uuid.uuid4()}{file_extension}"
    await save_upload_file(video, upload_path)

    # Create job
    job_id = create_job(
        job_type="preset_style",
        input_file=str(upload_path.name),
        preset=preset,
        format=format
    )

    # Start background processing
    background_tasks.add_task(
        process_preset_style,
        job_id,
        upload_path,
        preset,
        format,
        RESULTS_DIR
    )

    return {"job_id": job_id, "status": "processing"}


@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """Get job status."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")

    return jobs[job_id]


@app.get("/api/download/{job_id}")
async def download_result(job_id: str):
    """Download processed video."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")

    job = jobs[job_id]

    if job["status"] != JobStatus.COMPLETED:
        raise HTTPException(400, "Job not completed yet")

    result_file = RESULTS_DIR / job["result"]

    if not result_file.exists():
        raise HTTPException(404, "Result file not found")

    return FileResponse(
        result_file,
        media_type="video/mp4",
        filename=result_file.name
    )


@app.get("/api/presets")
async def get_presets():
    """Get list of preset styles."""
    presets = []
    for style_name in list_preset_styles():
        style = get_preset_style(style_name)
        presets.append({
            'id': style_name,
            'name': style.name,
            'description': style.description,
            'pace': style.pace,
            'caption_style': style.caption_style,
            'color_grade': style.color_grade,
        })
    return presets


@app.delete("/api/job/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its files."""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")

    job = jobs[job_id]

    # Delete uploaded files
    if "input_file" in job:
        input_path = UPLOAD_DIR / job["input_file"]
        if input_path.exists():
            input_path.unlink()

    if "reference_file" in job:
        ref_path = UPLOAD_DIR / job["reference_file"]
        if ref_path.exists():
            ref_path.unlink()

    # Delete result file
    if "result" in job and job["result"]:
        result_path = RESULTS_DIR / job["result"]
        if result_path.exists():
            result_path.unlink()

    # Delete style file
    if "style_file" in job and job["style_file"]:
        style_path = STYLES_DIR / job["style_file"]
        if style_path.exists():
            style_path.unlink()

    # Remove job from memory
    del jobs[job_id]

    return {"message": "Job deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
