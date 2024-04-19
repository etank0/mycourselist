import React from 'react';
import "./HomeCard.css";
import axios from 'axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const AdminHomeCard = ({ course }) => {
  const navigate = useNavigate();
  const handleClick = async () => {
    const userid = JSON.parse(localStorage.getItem('user')).user_id;
    try {
      const response = await axios.get('http://localhost:4000/admin/delete/' + course.id);
      
      const { data } = response;

      console.log(data);
      
      console.log('Course removal successful');
      toast.success("Course Successfully Removed!");
      navigate("/");
    } catch (error) {
        console.error("Couldn't remove course:", error);
        toast.error("Couldn't remove course!");
    }
  }  
  return (
    <div className="home-card">
      <img src={course.thumbnail} alt={course.name} />
      <div className="course-details">
        <h3>{course.name}</h3>
        <p>Creator: {course.creator}</p>
        <p>Hours: {course.hours}</p>
        <a href={course.link} className='btn btn-primary' target="_blank" rel="noopener noreferrer">View Course</a>
        <a onClick={handleClick} className='btn btn-danger' target="_blank" rel="noopener noreferrer">Remove Course</a>
      </div>
    </div>
  );
}

export default AdminHomeCard;