import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./AdminCourseForm.css";
import { toast } from 'react-toastify';

const AdminCourseForm = () => {
  const [link, setLink] = useState('');
  const [hours, setHours] = useState('');

  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('http://localhost:4000/admin/add', {
          link,
          hours
        });
        
        const { data } = response;

        console.log(data);
        
        console.log('Course Addition successful');
        toast.success("Course Added Successfully!");
        navigate("/home");
    } catch (error) {
        console.error('Course Addition failed:', error);
        toast.error("Couldn't Add Course!");
    }

    // Reset form fields
    setLink('');
    setHours('');
  };

  return (
    <div className='admin-course-form'>
      <form onSubmit={handleSubmit}>
        <h2>Add Course</h2>
        <div className='mb-3'>
          <label className="form-label" htmlFor="course-link">Playlist Link:</label>
          <input
            className='form-control'
            type="text"
            id="course-link"
            value={link}
            onChange={(e) => setLink(e.target.value)}
          />
        </div>
        <div className='mb-3'>
          <label htmlFor="course-hours">Hours:</label>
          <input
            className='form-control'
            type="number"
            id="course-hours"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" type="submit">Add Course</button>
      </form>
    </div>
  );
};

export default AdminCourseForm;