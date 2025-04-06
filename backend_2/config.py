import os
from pymongo import MongoClient

# MongoDB Configuration
MONGODB_CONNECTION_STRING = "mongodb+srv://yashrahate2:rahate1234@cluster0.s4e7m.mongodb.net/"
DB_NAME = "FaceDetection"

# Create MongoDB client
mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]

# Collection names
STUDENTS_COLLECTION = "students"
EMBEDDINGS_COLLECTION = "embeddings"

# File storage paths
UPLOAD_FOLDER = 'uploads'
TEMP_GROUP_FOLDER = os.path.join(UPLOAD_FOLDER, 'group_photos')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_GROUP_FOLDER, exist_ok=True)

# Face recognition settings
FACE_RECOGNITION_MODEL = "Facenet"
DISTANCE_METRIC = "cosine"
RECOGNITION_THRESHOLD = 0.5  # Threshold for face match (lower is more strict)