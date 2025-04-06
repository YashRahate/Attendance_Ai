// src/components/FaceCapture.jsx
import { useState, useRef , useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

const FaceCapture = ({navigateTo}) => {

  const location = useLocation(); // Add this
  const studentData = location.state?.studentData; // Get data from router state
  const navigate = useNavigate();
  const [currentImage, setCurrentImage] = useState(0);
  const [images, setImages] = useState(Array(5).fill(null));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (!studentData) {
      setError('Missing student information. Please go back and fill the registration form.');
      // Optionally navigate back: navigate(-1);
    }
  }, [studentData, navigate]);

  const handleImageSelect = async (e) => {
    if (!e.target.files || !e.target.files[0]) return;
    
    const file = e.target.files[0];
    setLoading(true);
    setError('');
    
    // Create form data
    const formData = new FormData();
    formData.append('image', file);
    formData.append('name', studentData.name);
    formData.append('roll_no', studentData.rollNo);
    formData.append('class', studentData.class);
    formData.append('imageIndex', currentImage);
    
    try {
      const response = await fetch('http://localhost:5000/api/upload-face', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Update images array with the file object
        const newImages = [...images];
        newImages[currentImage] = file;
        setImages(newImages);
        
        setSuccess(`Image ${currentImage + 1} uploaded successfully!`);
        
        // If this is the last image, wait a moment then proceed
        if (currentImage === 4) {
          setTimeout(() => {
            navigate(navigateTo);
          }, 1500);
        } else {
          // Move to next image
          setTimeout(() => {
            setCurrentImage(currentImage + 1);
            setSuccess('');
          }, 1000);
        }
      } else {
        setError(data.message || 'Failed to upload image');
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
      <h2 className="text-xl font-semibold mb-4">Face Image Capture</h2>
      <p className="mb-4">
        Please provide 5 clear images of your face. Each image will be checked for quality.
      </p>
      
      <div className="mb-6">
        <h3 className="text-lg font-medium mb-2">Progress: {currentImage + 1}/5</h3>
        <div className="flex justify-between mb-2">
          {[0, 1, 2, 3, 4].map((index) => (
            <div 
              key={index}
              className={`w-16 h-16 rounded-full flex items-center justify-center border-2 ${
                index < currentImage 
                  ? 'bg-green-100 border-green-500' 
                  : index === currentImage 
                    ? 'bg-blue-100 border-blue-500 animate-pulse' 
                    : 'bg-gray-100 border-gray-300'
              }`}
            >
              {index < currentImage ? (
                <span className="text-green-500 text-xl">✓</span>
              ) : (
                index + 1
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-medium mb-2">Image Guidelines:</h3>
        <ul className="list-disc pl-5">
          <li>Ensure your face is clearly visible</li>
          <li>Good lighting conditions</li>
          <li>Only one person in the frame</li>
          <li>Look directly at the camera</li>
          <li>Different angles are good for recognition quality</li>
        </ul>
      </div>
      
      <input 
        type="file" 
        ref={fileInputRef}
        accept="image/*"
        className="hidden"
        onChange={handleImageSelect}
      />
      
      <button 
        onClick={triggerFileInput}
        disabled={loading}
        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
      >
        {loading ? 'Processing...' : `Upload Face Image ${currentImage + 1}`}
      </button>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">
          {success}
        </div>
      )}
    </div>
  );
};

export default FaceCapture;