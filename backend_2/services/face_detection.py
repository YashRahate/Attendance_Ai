import cv2
import numpy as np

class FaceDetectionService:
    @staticmethod
    def detect_face(image_path):
        """
        Detects if there's exactly one face in the image with good conditions
        Returns: (success, message)
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False, "Failed to read image"
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Use haar cascade for quick face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return False, "No face detected"
            if len(faces) > 1:
                return False, "Multiple faces detected"
            
            # Check image brightness
            brightness = np.mean(gray)
            if brightness < 50:
                return False, "Poor lighting conditions"
                
            return True, "Face detected successfully"
        except Exception as e:
            return False, f"Error: {str(e)}"