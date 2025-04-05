// src/App.jsx
import { useState } from 'react';
import './App.css';
import RegistrationForm from './components/RegistrationForm';
import FaceCapture from './components/FaceCapture';
import GroupRecognition from './components/GroupRecognition';

function App() {
  const [step, setStep] = useState('registration');
  const [studentData, setStudentData] = useState({
    name: '',
    rollNo: '',
    class: ''
  });
  const [recognizedStudents, setRecognizedStudents] = useState([]);

  const handleStudentDataSubmit = (data) => {
    setStudentData(data);
    setStep('faceCapture');
  };

  const handleFaceCaptureComplete = () => {
    setStep('groupRecognition');
  };

  const handleRecognitionComplete = (students) => {
    setRecognizedStudents(students);
    setStep('results');
  };

  const resetApp = () => {
    setStep('registration');
    setStudentData({
      name: '',
      rollNo: '',
      class: ''
    });
    setRecognizedStudents([]);
  };

  return (
    <div className="container mx-auto p-4 max-w-xl">
      <h1 className="text-2xl font-bold mb-6 text-center">Face Recognition System</h1>
      
      {step === 'registration' && (
        <RegistrationForm onSubmit={handleStudentDataSubmit} />
      )}
      
      {step === 'faceCapture' && (
        <FaceCapture 
          studentData={studentData}
          onComplete={handleFaceCaptureComplete}
        />
      )}
      
      {step === 'groupRecognition' && (
        <GroupRecognition onRecognitionComplete={handleRecognitionComplete} />
      )}
      
      {step === 'results' && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Recognition Results</h2>
          {recognizedStudents.length > 0 ? (
            <>
              <p className="mb-4">The following students were recognized:</p>
              <ul className="list-disc pl-5 mb-6">
                {recognizedStudents.map((student, index) => (
                  <li key={index} className="mb-2">
                    <strong>{student.name}</strong> (Roll No: {student.roll_no}, Class: {student.class})
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="mb-6">No students were recognized in the group photo.</p>
          )}
          <button 
            onClick={resetApp}
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          >
            Start Over
          </button>
        </div>
      )}
    </div>
  );
}

export default App;