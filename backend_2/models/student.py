from config import db, STUDENTS_COLLECTION
from bson import ObjectId
from datetime import datetime  # Change this import
class Student:
    """Model for student information in MongoDB"""
    
    collection = db[STUDENTS_COLLECTION]
    
    @staticmethod
    def create(name, roll_no, division):
        """Create a new student record"""
        student_data = {
            "name": name,
            "roll_no": roll_no,
            "division": division,
            "created_at": datetime.now()
        }
        
        result = Student.collection.insert_one(student_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_by_id(student_id):
        """Get student by ID"""
        return Student.collection.find_one({"_id": ObjectId(student_id)})
    
    @staticmethod
    def get_by_roll_no(roll_no):
        """Get student by roll number"""
        return Student.collection.find_one({"roll_no": roll_no})
    
    @staticmethod
    def get_by_division(division):
        """Get all students in a division"""
        return list(Student.collection.find({"division": division}))
    
    @staticmethod
    def get_all():
        """Get all students"""
        return list(Student.collection.find())