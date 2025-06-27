# fabric_preprocessing.py
import cv2
import numpy as np
from PIL import Image

def enhance_for_defect_detection(image_path, output_path=None, method="all"):
    """
    Enhance fabric image to improve defect detection with YOLO v8
    
    Args:
        image_path: Path to input image
        output_path: Path to save output (optional)
        method: Enhancement method ("resize", "contrast", "edges", "all")
        
    Returns:
        Path to enhanced image
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return None
    
    # Choose enhancement method
    if method == "resize" or method == "all":
        # Simple upscaling
        img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2), interpolation=cv2.INTER_CUBIC)
    
    if method == "contrast" or method == "all":
        # Enhance contrast using CLAHE
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    if method == "edges" or method == "all":
        # Edge enhancement
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.dilate(edges, None)
        
        # Combine with original
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        img = cv2.addWeighted(img, 0.7, edges_colored, 0.3, 0)
    
    # Save if output path provided
    if output_path:
        cv2.imwrite(output_path, img)
        return output_path
    else:
        # Generate output path
        import os
        base, ext = os.path.splitext(image_path)
        new_path = f"{base}_enhanced{ext}"
        cv2.imwrite(new_path, img)
        return new_path

def prepare_for_yolo(image_path, size=(640, 640)):
    """
    Prepare image for YOLO v8 inference
    
    Args:
        image_path: Path to input image
        size: Target size for YOLO
        
    Returns:
        Preprocessed image as numpy array
    """
    # Read image
    img = cv2.imread(image_path)
    
    # Resize to YOLO input size
    img = cv2.resize(img, size)
    
    # Convert to RGB (YOLO uses RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Normalize pixel values
    img = img.astype(np.float32) / 255.0
    
    return img