import os
import uuid
from flask import request, jsonify
from services.recognition_service import RecognitionService
from config import TEMP_GROUP_FOLDER

def register_recognition_routes(app):
    @app.route('/api/recognize-group', methods=['POST'])
    def recognize_group():
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image provided"}), 400
        
        # Check if division was provided
        division = request.form.get('division', None)
        
        image = request.files['image']
        
        # Save the group image temporarily
        image_filename = f"group_{uuid.uuid4()}.jpg"
        group_image_path = os.path.join(TEMP_GROUP_FOLDER, image_filename)
        image.save(group_image_path)
        
        try:
            # Perform face recognition
            recognized_students = RecognitionService.recognize_faces_in_group(
                group_image_path, division
            )
            
            # Return results
            return jsonify({
                "success": True,
                "recognized_students": recognized_students,
                "total_recognized": len(recognized_students)
            })
        
        except Exception as e:
            # Clean up in case of error
            if os.path.exists(group_image_path):
                os.remove(group_image_path)
            
            return jsonify({
                "success": False,
                "message": f"Recognition error: {str(e)}"
            }), 500
        
        finally:
            # Optionally, you can choose to keep or delete the group photo here
            # If you want to delete:
            # if os.path.exists(group_image_path):
            #     os.remove(group_image_path)
            pass