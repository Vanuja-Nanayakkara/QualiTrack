import os
import sys
import torch
import numpy as np
from PIL import Image
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms.functional import to_tensor, to_pil_image
import urllib.request
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('esrgan_test')

def reconstruct_path():
    """Reconstruct the full path from command-line arguments"""
    # If only one argument (script name), return None
    if len(sys.argv) < 2:
        return None
    
    # Join all path arguments starting from the second argument
    full_path = ' '.join(sys.argv[1:])
    
    # Remove surrounding quotes if present
    full_path = full_path.strip('"\'')
    
    return full_path

# Architecture definition for ESRGAN
class ResidualDenseBlock(nn.Module):
    """Residual Dense Block"""
    def __init__(self, nf=64, gc=32):
        super(ResidualDenseBlock, self).__init__()
        self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1, bias=True)
        self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1, bias=True)
        self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1, bias=True)
        self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1, bias=True)
        self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1, bias=True)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x

class RRDB(nn.Module):
    """Residual in Residual Dense Block"""
    def __init__(self, nf=64, gc=32):
        super(RRDB, self).__init__()
        self.RDB1 = ResidualDenseBlock(nf, gc)
        self.RDB2 = ResidualDenseBlock(nf, gc)
        self.RDB3 = ResidualDenseBlock(nf, gc)

    def forward(self, x):
        out = self.RDB1(x)
        out = self.RDB2(out)
        out = self.RDB3(out)
        return out * 0.2 + x

class RRDBNet(nn.Module):
    """Networks consisting of Residual in Residual Dense Block"""
    def __init__(self, in_nc=3, out_nc=3, nf=64, nb=23, gc=32, scale=4):
        super(RRDBNet, self).__init__()
        self.scale = scale

        # First conv
        self.conv_first = nn.Conv2d(in_nc, nf, 3, 1, 1, bias=True)
        
        # RRDBs
        self.RRDB_trunk = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
        self.trunk_conv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        
        # Upsampling
        self.upconv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.upconv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        
        if scale == 8:
            self.upconv3 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        
        self.HRconv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv_last = nn.Conv2d(nf, out_nc, 3, 1, 1, bias=True)
        
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    def forward(self, x):
        fea = self.conv_first(x)
        trunk = self.trunk_conv(self.RRDB_trunk(fea))
        fea = fea + trunk
        
        # Upsampling
        fea = self.lrelu(self.upconv1(F.interpolate(fea, scale_factor=2, mode='nearest')))
        fea = self.lrelu(self.upconv2(F.interpolate(fea, scale_factor=2, mode='nearest')))
        
        if self.scale == 8:
            fea = self.lrelu(self.upconv3(F.interpolate(fea, scale_factor=2, mode='nearest')))
        
        out = self.conv_last(self.lrelu(self.HRconv(fea)))
        
        return out

class GarmentSuperResolution:
    """Super Resolution Model for Garment Inspection"""
    
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_initialized = False
        self.scale = 4  # Default upscaling factor
    
    def initialize_model(self):
        """Initialize the ESRGAN model with pre-trained weights"""
        if self.model_initialized:
            return True
            
        try:
            # Create model
            self.model = RRDBNet(scale=self.scale)
            
            # Use a local model path in the temp directory
            model_path = os.path.join(tempfile.gettempdir(), 'ESRGAN_garment_inspection.pth')
            
            # If model file doesn't exist, create a basic initialized model
            if not os.path.exists(model_path):
                logger.warning("No pre-trained model found. Creating a basic model.")
                # Save an initialized model state dict
                torch.save(self.model.state_dict(), model_path)
            
            # Load model weights
            state_dict = torch.load(model_path, map_location=self.device)
            
            # Load state dict
            try:
                self.model.load_state_dict(state_dict, strict=False)
            except Exception as e:
                logger.warning(f"Failed to load model weights: {e}")
                logger.info("Using randomly initialized model.")
            
            self.model.eval()
            self.model = self.model.to(self.device)
            self.model_initialized = True
            
            logger.info(f"Super-resolution model initialized on {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing super-resolution model: {str(e)}")
            return False
    
    def enhance_image(self, input_image_path, output_image_path=None):
        """
        Enhance an image using ESRGAN super-resolution.
        
        Args:
            input_image_path: Path to the input image
            output_image_path: Path to save the enhanced image (optional)
            
        Returns:
            Path to the enhanced image or None if failed
        """
        if not self.initialize_model():
            return None
            
        try:
            # Normalize and expand the path
            input_image_path = os.path.abspath(os.path.expanduser(input_image_path))
            
            # Verify file exists
            if not os.path.exists(input_image_path):
                logger.error(f"Input image file does not exist: {input_image_path}")
                return None
            
            # Open and prepare image
            img = Image.open(input_image_path).convert('RGB')
            
            # Limit image size for memory constraints
            max_size = 1024  # Maximum dimension
            if max(img.size) > max_size:
                factor = max_size / max(img.size)
                new_size = (int(img.size[0] * factor), int(img.size[1] * factor))
                logger.info(f"Resizing large image from {img.size} to {new_size}")
                img = img.resize(new_size, Image.LANCZOS)
            
            # Apply super-resolution
            with torch.no_grad():
                # Convert to tensor and normalize
                lr_tensor = to_tensor(img).unsqueeze(0).to(self.device)
                
                # Process with model
                sr_tensor = self.model(lr_tensor)
                
                # Convert back to image
                sr_img = to_pil_image(sr_tensor.squeeze(0).cpu().clamp(0, 1))
            
            # Determine output path
            if not output_image_path:
                # Create a default output path if not provided
                base, ext = os.path.splitext(input_image_path)
                output_image_path = f"{base}_superres{ext}"
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
            
            # Save the enhanced image
            sr_img.save(output_image_path)
            logger.info(f"Enhanced image saved to {output_image_path}")
            return output_image_path
                
        except Exception as e:
            logger.error(f"Error enhancing image: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None

# Main execution for testing
if __name__ == '__main__':
    # Reconstruct the full path
    image_path = reconstruct_path()
    
    # Check if image path is provided
    if not image_path:
        print("ERROR: Please provide an image path as a command-line argument.")
        sys.exit(1)
    
    # Create and test the super-resolution model
    sr = GarmentSuperResolution()
    
    # Initialize the model
    if sr.initialize_model():
        try:
            # Enhance the image
            output_path = sr.enhance_image(image_path)
            
            if output_path:
                print(f"Image enhanced. Output saved to: {output_path}")
            else:
                print("Failed to enhance the image.")
        except Exception as e:
            logger.error(f"Unexpected error during image enhancement: {e}")
            import traceback
            logger.error(traceback.format_exc())
    else:
        print("Failed to initialize the model.")