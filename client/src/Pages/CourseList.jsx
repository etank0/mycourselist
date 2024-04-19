import React from 'react'
import "./UserHome.css";
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ListCard from '../Components/ListCard';

function CourseList() {
    const [courses, setCourses] = useState('');
    const [user, setUser] = useState('');
    const { username } = useParams();
    const fetchData = async () => {
      try {
          
          console.log(username);
          const response = await axios.get('http://localhost:4000/courselist/' + username);
          
          const { data } = response;
  
          console.log(data.courses);
          setCourses(data.courses);
          setUser(data.user);
          console.log("Courses fetched successfully!");
      } catch (error) {
          console.error("Couldn't fetch courses:", error);
      }
    } 
    useEffect(() => {
          fetchData();
      }, []);
  
    return (
        <div className="outer-container">
            <h3>
                Viewing {user.name}'s{`(${user.username})`} Course List
            </h3>
            <div className='catalog-container'>
                {
                    courses ? 
                        courses.map(course => {
                            return <ListCard key={course.id} course={course}/>
                        })
                    :
                    <></>
                }
            </div>
        </div>
    )
  };

export default CourseList