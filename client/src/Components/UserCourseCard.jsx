import React from 'react';
import "./UserCourseCard.css";
import axios from 'axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const UserCourseCard = ({ course }) => {
  const navigate = useNavigate();
  const handleClick = async () => {
    const userid = JSON.parse(localStorage.getItem('user')).user_id;
    try {
      const response = await axios.post('http://localhost:4000/user/enroll', {
        userid,
        courseid: course.id
      });
      
      const { data } = response;

      console.log(data);
      
      console.log('Course addition successful');
      toast.success("Course Successfully Added!");
      navigate("/");
    } catch (error) {
        console.error("Couldn't add course:", error);
        toast.error("Couldn't add course!");
    }
  }  
  return (
    <div className="course-card">
      <img src={course.thumbnail} alt={course.name} />
      <div className="course-details">
        <h3>{course.name}</h3>
        <p>Creator: {course.creator}</p>
        <p>Hours: {course.hours}</p>
        <a href={course.link} className='btn btn-primary' target="_blank" rel="noopener noreferrer">View Course</a>
        <a onClick={handleClick} className='btn btn-primary' target="_blank" rel="noopener noreferrer">Add Course</a>
      </div>
    </div>
  );
}

export default UserCourseCard;