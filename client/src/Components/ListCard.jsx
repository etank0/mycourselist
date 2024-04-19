import React from 'react';
import "./HomeCard.css";

const ListCard = ({ course }) => {
  return (
    <div className="home-card">
      <img src={course.thumbnail} alt={course.name} />
      <div className="course-details">
        <h3>{course.name}</h3>
        <p>Creator: {course.creator}</p>
        <p>Hours: {course.hours}</p>
        <a href={course.link} className='btn btn-primary' target="_blank" rel="noopener noreferrer">View Course</a>
      </div>
    </div>
  );
}

export default ListCard;