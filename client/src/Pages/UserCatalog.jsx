import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "./UserCatalog.css";
import { toast } from 'react-toastify';
import "./UserCatalog.css";
import UserCourseCard from '../Components/UserCourseCard';


const UserCatalog = (props) => {
  const [courses, setCourses] = useState('');
  const user = JSON.parse(localStorage.getItem('user'));
  const fetchData = async () => {
    try {
        
        console.log(user);
        const response = await axios.get('http://localhost:4000/user/get/' + user.user_id);
        
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
                    return <UserCourseCard key={course.id} course={course}/>
                })
            :
            <></>
        }
    </div>
  )
};

export default UserCatalog;