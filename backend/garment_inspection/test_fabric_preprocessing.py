# test_complete_preprocessing.py
import cv2
import time
import os
import numpy as np

def enhance_fabric_image(image_path, output_path=None):
    start_time = time.time()
    print(f"Processing image: {image_path}")
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return None
    
    print(f"Original image size: {img.shape}")
    
    # Step 1: Resize (2x)
    start_step = time.time()
    img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2), interpolation=cv2.INTER_CUBIC)
    print(f"Resize completed in {time.time() - start_step:.2f} seconds. New size: {img.shape}")
    
    # Step 2: Enhance contrast
    start_step = time.time()
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    print(f"Contrast enhancement completed in {time.time() - start_step:.2f} seconds")
    
    # Step 3: Edge enhancement
    start_step = time.time()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges = cv2.dilate(edges, None)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    img = cv2.addWeighted(img, 0.8, edges_colored, 0.2, 0)
    print(f"Edge enhancement completed in {time.time() - start_step:.2f} seconds")
    
    # Generate output path if not provided
    if not output_path:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_enhanced{ext}"
    
    # Save result
    start_step = time.time()
    cv2.imwrite(output_path, img)
    print(f"Image saved to {output_path} in {time.time() - start_step:.2f} seconds")
    
    total_time = time.time() - start_time
    print(f"Total processing time: {total_time:.2f} seconds")
    
    return output_path

if __name__ == "__main__":
    test_image = "C:/Programming/Cloned Shii/Final/Automated-7-0-Inspection-System/backend/Hole.png0"
    enhanced_image = enhance_fabric_image(test_image)