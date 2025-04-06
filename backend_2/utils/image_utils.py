import cv2
import numpy as np
import os

def ensure_image_quality(image_path, min_size=(64, 64), min_brightness=50):
    """
    Check if image meets minimum quality requirements
    
    Args:
        image_path: Path to the image file
        min_size: Minimum dimensions (width, height)
        min_brightness: Minimum average brightness (0-255)
        
    Returns:
        (meets_requirements, message)
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to read image"
        
        # Check dimensions
        height, width = img.shape[:2]
        if width < min_size[0] or height < min_size[1]:
            return False, f"Image too small. Minimum size: {min_size[0]}x{min_size[1]}"
        
        # Check brightness
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        if brightness < min_brightness:
            return False, f"Image too dark. Brightness: {brightness:.1f}, Minimum: {min_brightness}"
            
        return True, "Image meets quality requirements"
    except Exception as e:
        return False, f"Error checking image quality: {str(e)}"

def clean_temp_files(directory, pattern=None):
    """
    Clean temporary files from a directory
    
    Args:
        directory: Directory to clean
        pattern: Optional filename pattern to match (e.g., '*.jpg')
    """
    try:
        import glob
        if pattern:
            files = glob.glob(os.path.join(directory, pattern))
        else:
            files = [os.path.join(directory, f) for f in os.listdir(directory) 
                    if os.path.isfile(os.path.join(directory, f))]
        
        for file_path in files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")
                
        return len(files)
    except Exception as e:
        print(f"Error cleaning directory {directory}: {e}")
        return 0