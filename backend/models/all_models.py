from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum

class EvaluationStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    frame_folder = Column(String, nullable=True)
    fps = Column(Float, nullable=True)
    total_frames = Column(Integer, nullable=True)
    progress = Column(Float, default=0.0)
    status = Column(SQLEnum(EvaluationStatus), default=EvaluationStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    evaluation = relationship("Evaluation", back_populates="video", uselist=False, cascade="all, delete-orphan")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), unique=True)
    status = Column(SQLEnum(EvaluationStatus), default=EvaluationStatus.pending)
    progress = Column(Float, default=0.0)
    mean_lpips = Column(Float, nullable=True)
    var_lpips = Column(Float, nullable=True)
    max_lpips = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    video = relationship("Video", back_populates="evaluation")
    results = relationship("Result", back_populates="evaluation", cascade="all, delete-orphan")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    frame_a = Column(String, nullable=False)
    frame_b = Column(String, nullable=False)
    lpips_score = Column(Float, nullable=False)
    
    evaluation = relationship("Evaluation", back_populates="results")
