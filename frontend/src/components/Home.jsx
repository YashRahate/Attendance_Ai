// src/components/Home.jsx
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Welcome to Face Recognition System</h2>
      <p className="mb-6">
        This system allows you to register student faces and perform group face recognition.
      </p>
      
      <div className="space-y-4">
        <Link to="/registration">
          <button className="w-full bg-blue-500 text-white py-3 rounded hover:bg-blue-600">
            Register New Student
          </button>
        </Link>
        
        <Link to="/group-recognition">
          <button className="w-full bg-green-500 text-white py-3 rounded hover:bg-green-600">
            Group Recognition
          </button>
        </Link>
      </div>
      
      <div className="mt-8 p-4 bg-gray-100 rounded">
        <h3 className="font-medium mb-2">How it works:</h3>
        <ul className="list-disc pl-5">
          <li className="mb-2">
            <strong>Student Registration:</strong> Register student details and capture face images for the system
          </li>
          <li>
            <strong>Group Recognition:</strong> Upload a group photo to identify registered students
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Home;