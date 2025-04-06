from datetime import datetime
from bson import ObjectId
import numpy as np
from config import db, EMBEDDINGS_COLLECTION

class Embedding:
    """Model for facial embeddings in MongoDB"""
    
    collection = db[EMBEDDINGS_COLLECTION]
    
    @staticmethod
    def create(student_id, student_name, division, embedding_data):
        """
        Create a new embedding record
        
        Args:
            student_id: MongoDB ObjectId or string of the student
            student_name: Name of the student
            division: Class/division of the student
            embedding_data: List of 5 embedding arrays
        """
        if isinstance(student_id, str):
            student_id = ObjectId(student_id)
        
        # Convert numpy arrays to lists for MongoDB storage
        processed_embeddings = []
        for emb in embedding_data:
            if isinstance(emb, np.ndarray):
                processed_embeddings.append(emb.tolist())
            else:
                processed_embeddings.append(emb)
        
        embedding_doc = {
            "student_id": student_id,
            "student_name": student_name,
            "division": division,
            "embeddings": processed_embeddings,
            "created_at": datetime.now()
        }
        
        result = Embedding.collection.insert_one(embedding_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_student_id(student_id):
        """Get embeddings for a specific student"""
        if isinstance(student_id, str):
            student_id = ObjectId(student_id)
        
        return Embedding.collection.find_one({"student_id": student_id})
    
    @staticmethod
    def get_by_division(division):
        """Get all embeddings for students in a specific division"""
        return list(Embedding.collection.find({"division": division}))
    
    @staticmethod
    def get_all():
        """Get all embeddings"""
        return list(Embedding.collection.find())