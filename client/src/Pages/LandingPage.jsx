import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';
import logo from '../logo.png'

const LandingPage = () => {
  return (
    <div className="landing-page">
        <div className='text-box'>
            <h1>Welcome to Our Website</h1>
        </div>
        <div className="button-box">
            <div className="buttons-container">
                <img src={logo} alt="MyCourseList Logo" />
                <Link to="/user/login" className="btn btn-primary">User Login</Link>
                <Link to="/admin/login" className="btn btn-primary">Admin Login</Link>
                <Link to="/user/register" className="btn btn-primary">User Registration</Link>
            </div>
        </div>
    </div>
  );
};

export default LandingPage;
