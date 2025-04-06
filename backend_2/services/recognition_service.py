import os
import uuid
import numpy as np
import cv2
from deepface import DeepFace
from models.embedding import Embedding
from models.student import Student
from config import FACE_RECOGNITION_MODEL, DISTANCE_METRIC, RECOGNITION_THRESHOLD

class RecognitionService:
    @staticmethod
    def extract_faces_from_group(group_photo_path):
        """
        Extract faces from a group photo
        
        Returns:
            List of face objects
        """
        try:
            print("Extracting Faces")
            face_objs = DeepFace.extract_faces(
                img_path=group_photo_path,
                enforce_detection=True,
                detector_backend="opencv"
            )
            
            return face_objs
        except Exception as e:
            print(f"Error extracting faces: {str(e)}")
            return []
    
    @staticmethod
    def calculate_distance(embedding1, embedding2, metric="cosine"):
        """
        Calculate distance between two embeddings based on the specified metric
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            metric: Distance metric to use (cosine or euclidean)
            
        Returns:
            Calculated distance value
        """
        if metric == "cosine":
            # Normalize vectors to unit length
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 1.0  # Maximum distance if either vector is zero
                
            embedding1_norm = embedding1 / norm1
            embedding2_norm = embedding2 / norm2
            
            # Calculate cosine similarity
            cosine_sim = np.dot(embedding1_norm, embedding2_norm)
            
            # Convert to distance (1 - similarity)
            # Ensure distance is between 0 and 1
            return max(0, min(1, 1 - cosine_sim))
        else:
            # Euclidean distance
            return np.linalg.norm(embedding1 - embedding2)
    
    @staticmethod
    def compare_embedding_vectors(face_embedding, stored_embeddings, metric=DISTANCE_METRIC):
        """
        Compare a single face embedding against a set of stored embeddings
        
        Args:
            face_embedding: Embedding vector for a face from the group photo
            stored_embeddings: List of stored embeddings for a student
            metric: Distance metric to use
            
        Returns:
            (match_found, distance) - Boolean indicating if match was found, and the distance
        """
        # Convert stored embeddings back to numpy arrays if they're lists
        processed_stored_embeddings = []
        for emb in stored_embeddings:
            if isinstance(emb, list):
                processed_stored_embeddings.append(np.array(emb))
            else:
                processed_stored_embeddings.append(emb)
        
        # Compare against each stored embedding
        min_distance = float('inf')
        match_found = False
        
        for stored_emb in processed_stored_embeddings:
            # Calculate distance using proper metric calculation
            distance = RecognitionService.calculate_distance(face_embedding, stored_emb, metric)
            
            # Update minimum distance
            if distance < min_distance:
                min_distance = distance
            
            # Check if this is a match
            if distance < RECOGNITION_THRESHOLD:
                match_found = True
                break
        
        return match_found, min_distance
    
    @staticmethod
    def represent_face(face_img, enforce_detection=False):
        """
        Generate face embedding from a face image
        
        Args:
            face_img: Face image array
            enforce_detection: Whether to enforce face detection
            
        Returns:
            Face embedding vector
        """
        try:
            # Save face temporarily to disk (DeepFace needs a file path)
            temp_face_path = os.path.join('uploads', f"temp_face_{uuid.uuid4()}.jpg")
            cv2.imwrite(temp_face_path, face_img)
            
            # Generate embedding
            face_embedding_obj = DeepFace.represent(
                img_path=temp_face_path,
                model_name=FACE_RECOGNITION_MODEL,
                enforce_detection=enforce_detection
            )
            
            # Clean up temporary file
            if os.path.exists(temp_face_path):
                os.remove(temp_face_path)
            
            # Handle output format of DeepFace
            if isinstance(face_embedding_obj, list):
                face_embedding = face_embedding_obj[0]['embedding']
            else:
                face_embedding = face_embedding_obj['embedding']
                
            return np.array(face_embedding)
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            # Clean up temporary file if it exists
            if 'temp_face_path' in locals() and os.path.exists(temp_face_path):
                os.remove(temp_face_path)
            return None
    
    @staticmethod
    def recognize_faces_in_group(group_photo_path, division=None):
        """
        Recognize students in a group photo using stored embeddings

        Args:
            group_photo_path: Path to the group photo
            division: Optional division to filter embeddings

        Returns:
            List of recognized students
        """
        recognized_students = []
        seen_student_ids = set()  # To prevent duplicates

        try:
            # Extract faces from the group photo
            extracted_faces = RecognitionService.extract_faces_from_group(group_photo_path)

            if not extracted_faces or len(extracted_faces) == 0:
                print("No faces extracted.")
                return []
                
            print(f"Extracted {len(extracted_faces)} faces from group photo")

            # Load embeddings from MongoDB, filtered by division if provided
            if division:
                embeddings_list = Embedding.get_by_division(division)
                print(f"Loaded {len(embeddings_list)} embeddings for division {division}")
            else:
                embeddings_list = Embedding.get_all()
                print(f"Loaded {len(embeddings_list)} embeddings total")

            # For each face in the group photo
            for face_idx, face_obj in enumerate(extracted_faces):
                print(f"\nProcessing face {face_idx+1}/{len(extracted_faces)}")
                face_img = face_obj['face']

                try:
                    # Generate embedding for this face
                    face_embedding = RecognitionService.represent_face(face_img, enforce_detection=False)
                    
                    if face_embedding is None:
                        print(f"Could not generate embedding for face {face_idx+1}")
                        continue
                        
                    print(f"Generated embedding with shape {face_embedding.shape}")

                    # Track best match
                    best_match = None
                    best_match_distance = float('inf')
                    best_match_student_id = None

                    # Compare against each student's stored embeddings
                    for emb_doc in embeddings_list:
                        student_id = str(emb_doc['student_id'])
                        
                        if student_id in seen_student_ids:
                            continue

                        # Extract the embeddings correctly
                        stored_embeddings_np = []
                        for idx in range(len(emb_doc['embeddings'])):
                            # Handle possible different structures
                            if isinstance(emb_doc['embeddings'][idx], list) and len(emb_doc['embeddings'][idx]) > 0:
                                if isinstance(emb_doc['embeddings'][idx][0], dict) and 'embedding' in emb_doc['embeddings'][idx][0]:
                                    embedding_array = emb_doc['embeddings'][idx][0]['embedding']
                                    stored_embeddings_np.append(np.array(embedding_array))
                            elif isinstance(emb_doc['embeddings'][idx], dict) and 'embedding' in emb_doc['embeddings'][idx]:
                                embedding_array = emb_doc['embeddings'][idx]['embedding']
                                stored_embeddings_np.append(np.array(embedding_array))

                        if not stored_embeddings_np:
                            continue

                        # Compare embeddings
                        match_found, distance = RecognitionService.compare_embedding_vectors(
                            face_embedding, stored_embeddings_np, DISTANCE_METRIC
                        )

                        # Track best match even if below threshold
                        if distance < best_match_distance:
                            best_match_distance = distance
                            best_match_student_id = student_id
                            
                        # If match is found, add to recognized students
                        if match_found:
                            print(f"Match found for student {student_id} with distance {distance:.4f}")
                            student = Student.get_by_id(student_id)
                            if student:
                                student_info = {
                                    'name': student['name'],
                                    'roll_no': student['roll_no'],
                                    'class': student['division'],
                                    'confidence': round((1.0 - distance) * 100, 1)  # Convert to percentage
                                }
                                recognized_students.append(student_info)
                                seen_student_ids.add(student_id)
                                break
                    
                    # If no match was found but we have a best match that's close
                    if not match_found and best_match_student_id:
                        near_threshold = RECOGNITION_THRESHOLD * 1.2  # 20% buffer
                        if best_match_distance < near_threshold:
                            print(f"Near match for student {best_match_student_id} with distance {best_match_distance:.4f}")
                            student = Student.get_by_id(best_match_student_id)
                            if student:
                                student_info = {
                                    'name': student['name'],
                                    'roll_no': student['roll_no'],
                                    'class': student['division'],
                                    'confidence': round((1.0 - best_match_distance) * 100, 1),  # Convert to percentage
                                    'tentative': True  # Mark as tentative match
                                }
                                recognized_students.append(student_info)
                                seen_student_ids.add(best_match_student_id)

                except Exception as e:
                    print(f"Error processing face: {str(e)}")

            # Sort recognized students by confidence
            recognized_students.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            print(f"Recognition complete. Found {len(recognized_students)} students.")
            return recognized_students

        except Exception as e:
            print(f"Recognition error: {str(e)}")
            return []