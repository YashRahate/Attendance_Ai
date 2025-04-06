from flask import Flask
from flask_cors import CORS
import os
from datetime import datetime

# Import configuration
from config import mongo_client

# Import controllers
from controllers.student_controller import register_student_routes
from controllers.recognition_controller import register_recognition_routes

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register routes
register_student_routes(app)
register_recognition_routes(app)

# Simple health check route
@app.route('/health', methods=['GET'])
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)