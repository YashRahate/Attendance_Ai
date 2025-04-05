// src/components/Results.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const Results = ({ recognizedStudents, resetApp }) => {
  const navigate = useNavigate();

  const handleRestart = () => {
    resetApp();
    navigate('/register');
  };

  return (
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
        onClick={handleRestart}
        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
      >
        Start Over
      </button>
    </div>
  );
};

export default Results;
