import glob
import os
from typing import Dict, List, Tuple

import cv2
import lpips
import torch
from PIL import Image
from torchvision import transforms

# Initialize globally so it's only loaded once per worker
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
try:
    loss_fn_alex = lpips.LPIPS(net='alex').to(device)
    loss_fn_alex.eval()
except Exception as e:
    print(f"Failed to load LPIPS model: {e}")
    loss_fn_alex = None

def load_image_for_lpips(path: str) -> torch.Tensor:
    # Read original frame with OpenCV
    frame = cv2.imread(path)
    if frame is None:
        raise ValueError(f"Could not read image: {path}")
        
    # Replicate exact OpenCV crop and resize from the old extraction script
    if frame.shape[:2] != (512, 512):
        h, w = frame.shape[:2]
        min_dim = min(h, w)
        start_y = h // 2 - min_dim // 2
        start_x = w // 2 - min_dim // 2
        frame = frame[start_y:start_y+min_dim, start_x:start_x+min_dim]
        # CRITICAL: Original script used INTER_AREA for downsampling
        frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_AREA)
        
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image for PyTorch transforms
    img = Image.fromarray(frame_rgb)
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
    ])
    return transform(img).unsqueeze(0).to(device)

def evaluate_folder(folder_path: str, progress_callback=None) -> Tuple[List[Dict[str, float]], float, float, float]:
    """
    Evaluates temporal stability for all frames in a folder.
    Returns:
        (results_list, mean_lpips, var_lpips, max_lpips)
    """
    if loss_fn_alex is None:
        raise Exception("LPIPS model not initialized.")

    files = sorted(glob.glob(os.path.join(folder_path, "frame_*.png")))
    if len(files) < 2:
        raise Exception("Not enough frames for temporal evaluation.")

    results = []
    scores = []
    
    total_pairs = len(files) - 1
    last_reported_progress = 0.0
    
    with torch.no_grad(): 
        img_t0 = load_image_for_lpips(files[0])
        
        for i in range(total_pairs):
            path_a = files[i]
            path_b = files[i+1]
            
            img_t1 = load_image_for_lpips(path_b)
            
            dist = loss_fn_alex(img_t0, img_t1).item()
            scores.append(dist)
            
            results.append({
                'frame_a': os.path.basename(path_a),
                'frame_b': os.path.basename(path_b),
                'lpips_score': round(dist, 5)
            })
            
            if progress_callback:
                progress = min(100.0, ((i + 1) / total_pairs) * 100.0)
                if progress - last_reported_progress >= 5.0 or (i + 1) == total_pairs:
                    progress_callback(progress)
                    last_reported_progress = progress
                    
            img_t0 = img_t1

    if not scores:
        raise Exception("Failed to calculate any LPIPS scores.")
        
    import pandas as pd
    df = pd.Series(scores)
    
    mean_v = df.mean()
    var_v = df.var() if len(scores) > 1 else 0.0
    max_v = df.max()
    
    return results, float(mean_v), float(var_v), float(max_v)
