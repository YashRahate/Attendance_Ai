import os
import uuid
from flask import request, jsonify
from models.student import Student
from services.face_detection import FaceDetectionService
from services.embedding_service import EmbeddingService
from config import UPLOAD_FOLDER

def register_student_routes(app):
    @app.route('/api/upload-face', methods=['POST'])
    def upload_face():
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image provided"}), 400
        
        if 'name' not in request.form or 'roll_no' not in request.form or 'division' not in request.form:
            return jsonify({"success": False, "message": "Missing student information"}), 400
        
        image = request.files['image']
        name = request.form['name']
        roll_no = request.form['roll_no']
        division = request.form['division']
        image_index = int(request.form['imageIndex'])  # 0-4 for the 5 images
        
        # Create user folder if it doesn't exist
        user_folder = os.path.join(UPLOAD_FOLDER, f"{name}_{roll_no}")
        os.makedirs(user_folder, exist_ok=True)
        
        # Save the image
        image_path = os.path.join(user_folder, f"image_{image_index}.jpg")
        image.save(image_path)
        
        # Detect face
        is_valid, message = FaceDetectionService.detect_face(image_path)
        if not is_valid:
            os.remove(image_path)  # Remove invalid image
            return jsonify({"success": False, "message": message}), 400
        
        # Check if this is the first image (index 0), if so, register student in DB
        if image_index == 0:
            try:
                # Create student record
                student_id = Student.create(name, roll_no, division)
            except Exception as e:
                os.remove(image_path)  # Clean up on error
                return jsonify({"success": False, "message": f"Failed to register student: {str(e)}"}), 500
        
        # If this is the last image (index 4), create embeddings for all images
        if image_index == 4:
            # Get all image paths
            image_paths = [os.path.join(user_folder, f"image_{i}.jpg") for i in range(5)]
            
            # Verify all images exist
            if not all(os.path.exists(path) for path in image_paths):
                return jsonify({
                    "success": False, 
                    "message": "Not all required images are available. Please reupload missing images."
                }), 400
            
            # Get student ID from database
            student = Student.get_by_roll_no(roll_no)
            if not student:
                return jsonify({"success": False, "message": "Student not found in database"}), 404
            
            student_id = str(student['_id'])
            
            # Process images and create embeddings
            success, message = EmbeddingService.process_student_images(
                student_id, name, division, image_paths
            )
            
            if success:
                return jsonify({
                    "success": True, 
                    "message": "All images processed successfully and embeddings created"
                })
            else:
                return jsonify({
                    "success": False, 
                    "message": message
                }), 500
        
        return jsonify({
            "success": True, 
            "message": f"Image {image_index+1} uploaded and validated successfully"
        })