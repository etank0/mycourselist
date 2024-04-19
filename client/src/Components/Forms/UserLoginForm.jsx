import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./UserLoginForm.css";
import { toast } from 'react-toastify';

const UserLoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('http://localhost:4000/user/login', {
          username,
          password
        });
        
        const { data } = response;
        data.user.isAdmin = false;

        console.log(data.user);
        
        // Store data in localStorage
        localStorage.setItem('user', JSON.stringify(data.user));
        
        console.log('User login successful');
        console.log(JSON.parse(localStorage.getItem('user')));
        toast.success("Login Successful!");
        navigate("/");
    } catch (error) {
        console.error('User login failed:', error);
        toast.error("Couldn't Login!");
    }

    // Reset form fields
    setUsername('');
    setPassword('');
  };

  return (
    <div className='user-login-form'>
      <form onSubmit={handleSubmit}>
        <h2>User Login</h2>
        <div className='mb-3'>
          <label className="form-label" htmlFor="user-username">Username:</label>
          <input
            className='form-control'
            type="text"
            id="user-username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className='mb-3'>
          <label htmlFor="user-password">Password:</label>
          <input
            className='form-control'
            type="password"
            id="user-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" type="submit">Login</button>
      </form>
    </div>
  );
};

export default UserLoginForm;