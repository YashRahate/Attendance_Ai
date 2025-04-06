// src/components/Results.jsx
import { useNavigate } from 'react-router-dom';

const Results = ({ 
  title = "Results", 
  message = "", 
  recognizedStudents = [], 
  buttonText = "Start Over", 
  navigateTo = "/", 
  resetApp 
}) => {
  const navigate = useNavigate();

  const handleNavigation = () => {
    if (resetApp) {
      resetApp();
    }
    navigate(navigateTo);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      
      {message && <p className="mb-4">{message}</p>}
      
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
        recognizedStudents && !message && <p className="mb-6">No students were recognized in the group photo.</p>
      )}
      
      <button 
        onClick={handleNavigation}
        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
      >
        {buttonText}
      </button>
    </div>
  );
};

export default Results;