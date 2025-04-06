import os
import numpy as np
from deepface import DeepFace
from models.embedding import Embedding
from models.student import Student
from config import FACE_RECOGNITION_MODEL

class EmbeddingService:
    @staticmethod
    def create_embedding(image_path):
        """
        Creates facial embedding using FaceNet
        """
        try:
            embedding = DeepFace.represent(img_path=image_path, model_name=FACE_RECOGNITION_MODEL)
            return embedding
        except Exception as e:
            print(f"Error creating embedding: {str(e)}")
            return None
    
    @staticmethod
    def process_student_images(student_id, student_name, division, image_paths):
        """
        Process multiple images for a student and save their embeddings
        
        Args:
            student_id: ID of the student
            student_name: Name of the student
            division: Division/class of the student
            image_paths: List of paths to the student's face images
        
        Returns:
            (success, message)
        """
        try:
            # Generate embeddings for all images
            embeddings = []
            
            for img_path in image_paths:
                if os.path.exists(img_path):
                    embedding = EmbeddingService.create_embedding(img_path)
                    if embedding:
                        embeddings.append(embedding)
            
            # Check if we have enough embeddings
            if len(embeddings) != len(image_paths):
                return False, f"Could only generate {len(embeddings)} out of {len(image_paths)} embeddings"
            
            # Save embeddings to MongoDB
            embedding_id = Embedding.create(student_id, student_name, division, embeddings)
            
            # Delete the images after embeddings are created
            for img_path in image_paths:
                if os.path.exists(img_path):
                    os.remove(img_path)
                    
            return True, f"Embeddings created successfully with ID: {embedding_id}"
            
        except Exception as e:
            return False, f"Error processing student images: {str(e)}"