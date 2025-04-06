// src/components/GroupRecognition.jsx
import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const GroupRecognition = ({ onRecognitionComplete, navigateTo }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageSelect = (e) => {
    if (!e.target.files || !e.target.files[0]) return;
    
    const file = e.target.files[0];
    setSelectedImage(file);
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }
    
    setLoading(true);
    
    const formData = new FormData();
    formData.append('image', selectedImage);
    
    try {
      const response = await fetch('http://localhost:5000/api/recognize-group', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        onRecognitionComplete(data.recognized_students || []);
        navigate(navigateTo);
      } else {
        setError(data.message || 'Recognition failed');
      }
    } catch (err) {
      setError('Server error. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Group Photo Recognition</h2>
      <p className="mb-6">
        Upload a group photo with multiple people to recognize students who have registered in the system.
      </p>
      
      <div className="mb-6">
        <input 
          type="file" 
          ref={fileInputRef}
          accept="image/*"
          className="hidden"
          onChange={handleImageSelect}
        />
        
        <button 
          onClick={triggerFileInput}
          className="w-full bg-gray-200 text-gray-800 py-2 rounded hover:bg-gray-300 mb-3"
        >
          Select Group Photo
        </button>
        
        {selectedImage && (
          <div className="text-center text-green-600">
            Selected: {selectedImage.name}
          </div>
        )}
      </div>
      
      <button 
        onClick={handleUpload}
        disabled={loading || !selectedImage}
        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:bg-blue-300 mb-4"
      >
        {loading ? 'Processing...' : 'Recognize Faces'}
      </button>
      
      {error && (
        <div className="p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      
      <div className="mt-6 p-4 bg-gray-100 rounded">
        <h3 className="font-medium mb-2">Tips for best results:</h3>
        <ul className="list-disc pl-5">
          <li>Use a clear photo with good lighting</li>
          <li>Ensure faces are visible and not too small</li>
          <li>Avoid extreme angles or heavily obscured faces</li>
          <li>Higher resolution images yield better results</li>
        </ul>
      </div>
    </div>
  );
};

export default GroupRecognition;