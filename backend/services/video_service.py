import cv2
import os
import shutil
from typing import Tuple, Callable

def extract_all_frames(video_path: str, output_folder: str, progress_callback: Callable[[float], None] = None) -> Tuple[int, float]:
    """
    Extracts frames from a video at their original resolution.
    Returns:
        Tuple of (total_extracted_frames, fps)
    """
    
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise Exception(f"Cannot open video {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps != fps: # catch NaN or 0
        fps = 30.0
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        total_frames = 100 # fallback if unknown

    count = 0
    last_reported_progress = 0.0
    while True:
        success, frame = cap.read()
        
        if not success:
            break
            
        frame_name = os.path.join(output_folder, f"frame_{count:04d}.png")
        cv2.imwrite(frame_name, frame)
        
        count += 1
        
        if progress_callback:
            progress = min(100.0, (count / total_frames) * 100.0)
            if progress - last_reported_progress >= 5.0 or count == total_frames:
                progress_callback(progress)
                last_reported_progress = progress
            
    cap.release()
    return count, fps
