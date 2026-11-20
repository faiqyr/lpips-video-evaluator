import os
import io
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session

from api.deps import get_db
from models.all_models import Video, Evaluation, Result, EvaluationStatus
from schemas.all_schemas import (
    EvaluationResponse, EvaluationDetailResponse,
    BatchTriggerRequest, BatchTriggerResponse
)
from services.lpips_service import evaluate_folder

router = APIRouter()


def process_evaluation_background(evaluation_id: int, folder_path: str):
    """Run LPIPS evaluation in background thread."""
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        def progress_callback(progress_val: float):
            eval_record = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
            if eval_record:
                eval_record.progress = round(progress_val, 2)
                db.commit()

        results_list, mean_lpips, var_lpips, max_lpips = evaluate_folder(folder_path, progress_callback=progress_callback)

        evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if evaluation:
            evaluation.mean_lpips = mean_lpips
            evaluation.var_lpips = var_lpips
            evaluation.max_lpips = max_lpips
            evaluation.status = EvaluationStatus.completed
            evaluation.completed_at = datetime.utcnow()

            for res in results_list:
                db.add(Result(
                    evaluation_id=evaluation.id,
                    frame_a=res['frame_a'],
                    frame_b=res['frame_b'],
                    lpips_score=res['lpips_score']
                ))
            db.commit()
    except Exception as e:
        evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if evaluation:
            evaluation.status = EvaluationStatus.failed
            evaluation.error_message = str(e)
            db.commit()
        print(f"LPIPS evaluation failed for eval {evaluation_id}: {e}")
    finally:
        db.close()


@router.post("/trigger/{video_id}", response_model=EvaluationResponse)
def trigger_evaluation(video_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Trigger LPIPS evaluation for a single video."""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.status != EvaluationStatus.completed:
        raise HTTPException(status_code=400, detail="Video frames are not fully extracted yet.")

    # Remove existing evaluation if any
    existing_eval = db.query(Evaluation).filter(Evaluation.video_id == video_id).first()
    if existing_eval and existing_eval.status in [EvaluationStatus.pending, EvaluationStatus.processing]:
        raise HTTPException(status_code=400, detail="Evaluation is already in progress.")

    if existing_eval:
        db.delete(existing_eval)
        db.commit()

    evaluation = Evaluation(
        video_id=video_id,
        status=EvaluationStatus.processing
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    background_tasks.add_task(process_evaluation_background, evaluation.id, video.frame_folder)

    return evaluation


@router.post("/trigger-batch", response_model=BatchTriggerResponse)
def trigger_batch_evaluation(
    request: BatchTriggerRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger LPIPS evaluation for multiple videos at once."""
    triggered = []
    errors = []

    for video_id in request.video_ids:
        try:
            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                errors.append({"video_id": video_id, "error": "Video not found"})
                continue

            if video.status != EvaluationStatus.completed:
                errors.append({"video_id": video_id, "error": "Frames not extracted yet"})
                continue

            existing_eval = db.query(Evaluation).filter(Evaluation.video_id == video_id).first()
            if existing_eval and existing_eval.status in [EvaluationStatus.pending, EvaluationStatus.processing]:
                errors.append({"video_id": video_id, "error": "Already in progress"})
                continue

            if existing_eval:
                db.delete(existing_eval)
                db.commit()

            evaluation = Evaluation(
                video_id=video_id,
                status=EvaluationStatus.processing
            )
            db.add(evaluation)
            db.commit()
            db.refresh(evaluation)

            background_tasks.add_task(process_evaluation_background, evaluation.id, video.frame_folder)
            triggered.append(video_id)

        except Exception as e:
            errors.append({"video_id": video_id, "error": str(e)})

    return BatchTriggerResponse(triggered=triggered, errors=errors)


@router.get("/{video_id}", response_model=EvaluationDetailResponse)
def get_evaluation(video_id: int, db: Session = Depends(get_db)):
    """Get evaluation results for a video."""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    evaluation = db.query(Evaluation).filter(Evaluation.video_id == video_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return evaluation


@router.get("/export/excel")
def export_excel(
    video_ids: Optional[str] = Query(None, description="Comma-separated video IDs"),
    db: Session = Depends(get_db)
):
    """Export evaluation results as Excel (.xlsx) file."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    # Parse video IDs
    if video_ids:
        ids = [int(x.strip()) for x in video_ids.split(",") if x.strip()]
        evaluations = db.query(Evaluation).filter(
            Evaluation.video_id.in_(ids),
            Evaluation.status == EvaluationStatus.completed
        ).all()
    else:
        evaluations = db.query(Evaluation).filter(
            Evaluation.status == EvaluationStatus.completed
        ).all()

    if not evaluations:
        raise HTTPException(status_code=404, detail="No completed evaluations found")

    wb = openpyxl.Workbook()

    # --- Summary Sheet ---
    ws_summary = wb.active
    ws_summary.title = "Summary"

    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    summary_headers = ["No", "Video Name", "Mean LPIPS", "Variance (Flicker)", "Max LPIPS (Morphing)", "Total Frames", "Status"]
    for col, header in enumerate(summary_headers, 1):
        cell = ws_summary.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        cell.border = thin_border

    for idx, ev in enumerate(evaluations, 1):
        video = db.query(Video).filter(Video.id == ev.video_id).first()
        video_name = video.filename if video else f"Video {ev.video_id}"
        total_frames = video.total_frames if video else 0

        row_data = [idx, video_name, ev.mean_lpips, ev.var_lpips, ev.max_lpips, total_frames, ev.status.value]
        for col, val in enumerate(row_data, 1):
            cell = ws_summary.cell(row=idx + 1, column=col, value=val)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

    # Auto-width columns
    for col in ws_summary.columns:
        max_length = max(len(str(cell.value or "")) for cell in col)
        ws_summary.column_dimensions[col[0].column_letter].width = min(max_length + 4, 40)

    # --- Detail Sheets per video ---
    for ev in evaluations:
        video = db.query(Video).filter(Video.id == ev.video_id).first()
        video_name = video.filename if video else f"Video_{ev.video_id}"
        # Sanitize sheet name (max 31 chars, no special chars)
        sheet_name = video_name[:28].replace("/", "_").replace("\\", "_").replace(".", "_")

        ws = wb.create_sheet(title=sheet_name)

        detail_headers = ["No", "Frame A", "Frame B", "LPIPS Score"]
        for col, header in enumerate(detail_headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = thin_border

        results = db.query(Result).filter(Result.evaluation_id == ev.id).all()
        for ridx, r in enumerate(results, 1):
            row_data = [ridx, r.frame_a, r.frame_b, r.lpips_score]
            for col, val in enumerate(row_data, 1):
                cell = ws.cell(row=ridx + 1, column=col, value=val)
                cell.border = thin_border
                cell.alignment = Alignment(horizontal='center')

        for col in ws.columns:
            max_length = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_length + 4, 40)

    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="lpips_evaluation_results.xlsx"'}
    )
