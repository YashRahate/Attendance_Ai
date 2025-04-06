// src/components/RegistrationForm.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const RegistrationForm = ({ onSubmit, navigateTo }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    rollNo: '',
    class: ''
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.rollNo.trim()) {
      newErrors.rollNo = 'Roll No is required';
    }
    
    if (!formData.class.trim()) {
      newErrors.class = 'Class is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData);
      navigate(navigateTo);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Student Registration</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="name">
            Full Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={`w-full p-2 border rounded ${errors.name ? 'border-red-500' : 'border-gray-300'}`}
            placeholder="Enter your full name"
          />
          {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="rollNo">
            Roll Number
          </label>
          <input
            type="text"
            id="rollNo"
            name="rollNo"
            value={formData.rollNo}
            onChange={handleChange}
            className={`w-full p-2 border rounded ${errors.rollNo ? 'border-red-500' : 'border-gray-300'}`}
            placeholder="Enter your roll number"
          />
          {errors.rollNo && <p className="text-red-500 text-sm mt-1">{errors.rollNo}</p>}
        </div>
        
        <div className="mb-6">
          <label className="block text-gray-700 mb-2" htmlFor="class">
            Class
          </label>
          <input
            type="text"
            id="class"
            name="class"
            value={formData.class}
            onChange={handleChange}
            className={`w-full p-2 border rounded ${errors.class ? 'border-red-500' : 'border-gray-300'}`}
            placeholder="Enter your class"
          />
          {errors.class && <p className="text-red-500 text-sm mt-1">{errors.class}</p>}
        </div>
        
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          Next
        </button>
      </form>
    </div>
  );
};

export default RegistrationForm;