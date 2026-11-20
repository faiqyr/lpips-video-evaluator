from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from models.all_models import EvaluationStatus

# Video Schemas
class VideoResponse(BaseModel):
    id: int
    filename: str
    fps: Optional[float] = None
    total_frames: Optional[int] = None
    progress: Optional[float] = 0.0
    status: EvaluationStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Evaluation & Result Schemas
class ResultResponse(BaseModel):
    id: int
    evaluation_id: int
    frame_a: str
    frame_b: str
    lpips_score: float

    model_config = ConfigDict(from_attributes=True)

class EvaluationResponse(BaseModel):
    id: int
    video_id: int
    status: EvaluationStatus
    progress: Optional[float] = 0.0
    mean_lpips: Optional[float] = None
    var_lpips: Optional[float] = None
    max_lpips: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class EvaluationDetailResponse(EvaluationResponse):
    results: List[ResultResponse] = []

# Batch Schemas
class BatchTriggerRequest(BaseModel):
    video_ids: List[int]

class BatchTriggerResponse(BaseModel):
    triggered: List[int] = []
    errors: List[dict] = []
