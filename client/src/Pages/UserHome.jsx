import React from 'react'
import "./UserHome.css";
import HomeCard from '../Components/HomeCard';
import axios from 'axios';
import { useEffect, useState } from 'react';

function UserHome() {
    const [courses, setCourses] = useState('');
    const user = JSON.parse(localStorage.getItem('user'));
    const fetchData = async () => {
      try {
          
          console.log(user);
          const response = await axios.get('http://localhost:4000/courselist/' + user.username);
          
          const { data } = response;
  
          console.log(data.courses);
          setCourses(data.courses);
          console.log("Courses fetched successfully!");
      } catch (error) {
          console.error("Couldn't fetch courses:", error);
      }
    } 
    useEffect(() => {
          fetchData();
      }, []);
  
    return (
      <div className='catalog-container'>
          {
              courses ? 
                  courses.map(course => {
                      return <HomeCard key={course.id} course={course}/>
                  })
              :
              <></>
          }
      </div>
    )
  };

export default UserHome