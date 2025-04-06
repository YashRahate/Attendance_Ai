// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import './App.css';
import RegistrationForm from './components/RegistrationForm';
import FaceCapture from './components/FaceCapture';
import GroupRecognition from './components/GroupRecognition';
import Results from './components/Results';
import Home from './components/Home';

function App() {
  const [studentData, setStudentData] = useState({
    name: '',
    rollNo: '',
    class: ''
  });
  const [recognizedStudents, setRecognizedStudents] = useState([]);

  const handleStudentDataSubmit = (data) => {
    setStudentData(data);
  };

  const handleRecognitionComplete = (students) => {
    setRecognizedStudents(students);
  };

  const resetApp = () => {
    setStudentData({
      name: '',
      rollNo: '',
      class: ''
    });
    setRecognizedStudents([]);
  };

  return (
    <Router>
      <div className="container mx-auto p-4 max-w-xl">
        <h1 className="text-2xl font-bold mb-6 text-center">Face Recognition System</h1>
        
        <Routes>
          <Route path="/" element={<Home />} />
          
          <Route 
            path="/registration" 
            element={<RegistrationForm onSubmit={handleStudentDataSubmit} navigateTo="/face-capture" />} 
          />
          
          <Route 
            path="/face-capture" 
            element={
              studentData.name ? (
                <FaceCapture studentData={studentData} navigateTo="/student-results" />
              ) : (
                <Navigate to="/registration" replace />
              )
            } 
          />
          
          {/* Independent route for group recognition */}
          <Route 
            path="/group-recognition" 
            element={<GroupRecognition onRecognitionComplete={handleRecognitionComplete} navigateTo="/group-results" />} 
          />
          
          <Route 
            path="/student-results" 
            element={
              <Results 
                title="Registration Complete"
                message="Your face data has been successfully registered in the system."
                buttonText="Back to Home"
                navigateTo="/"
                resetApp={resetApp}
              />
            } 
          />
          
          <Route 
            path="/group-results" 
            element={
              <Results 
                title="Recognition Results"
                recognizedStudents={recognizedStudents}
                buttonText="Start New Recognition"
                navigateTo="/group-recognition"
                resetApp={resetApp}
              />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;