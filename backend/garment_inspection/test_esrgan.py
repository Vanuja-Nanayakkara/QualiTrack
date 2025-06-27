# test_esrgan.py - Save this file in your project directory
import os
import sys
import django
import time
from PIL import Image

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garment_inspection.settings')
django.setup()

# Import the super-resolution model after Django setup
from inspection.esrgan import GarmentSuperResolution

def test_super_resolution(input_image_path):
    """Test the ESRGAN super-resolution model with an input image."""
    print(f"Testing ESRGAN super-resolution with image: {input_image_path}")
    
    # Check if file exists
    if not os.path.exists(input_image_path):
        print(f"Error: File {input_image_path} not found")
        return
    
    # Get original image dimensions
    with Image.open(input_image_path) as img:
        original_width, original_height = img.size
    
    print(f"Original image dimensions: {original_width}x{original_height}")
    
    # Initialize model
    print("Initializing ESRGAN super-resolution model...")
    sr_model = GarmentSuperResolution()
    
    # Apply super-resolution
    print("Applying super-resolution enhancement...")
    start_time = time.time()
    output_path = os.path.splitext(input_image_path)[0] + '_enhanced' + os.path.splitext(input_image_path)[1]
    enhanced_path = sr_model.enhance_image(input_image_path, output_path)
    end_time = time.time()
    
    if enhanced_path:
        print(f"Image enhanced successfully in {end_time - start_time:.2f} seconds")
        print(f"Enhanced image saved to: {enhanced_path}")
        
        # Get enhanced image dimensions
        with Image.open(enhanced_path) as img:
            enhanced_width, enhanced_height = img.size
        
        print(f"Enhanced image dimensions: {enhanced_width}x{enhanced_height}")
        print(f"Scale factors: {enhanced_width/original_width:.1f}x width, {enhanced_height/original_height:.1f}x height")
    else:
        print("Failed to enhance image")

if __name__ == "__main__":
    # Check if image path is provided as command line argument
    if len(sys.argv) < 2:
        print("Usage: python test_esrgan.py <path_to_image>")
        sys.exit(1)
    
    test_super_resolution(sys.argv[1])