import React from 'react'
import AdminHome from './AdminHome';
import UserHome from './UserHome';

function HomePage(props) {
    const { user } = props; 
  return (
    <>
        {
            user.isAdmin ?
            <AdminHome /> :
            <UserHome />
        }
    </>
    
  )
}

export default HomePage