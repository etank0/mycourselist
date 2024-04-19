import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./UserRegisterForm.css";
import { toast } from 'react-toastify';

const UserRegisterForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repassword, setRePassword] = useState('');
  const [name, setName] = useState('');

  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('http://localhost:4000/user/register', {
          username,
          password,
          repassword,
          name
        });
        
        const { data } = response;

        console.log(data);
        
        console.log('User registration successful');
        toast.success("User Registered Successfully!");
        navigate("/home");
    } catch (error) {
        console.error('User Registration failed:', error);
        toast.error("Couldn't Register!");
    }

    // Reset form fields
    setUsername('');
    setPassword('');
    setRePassword('');
    setName('');
  };

  return (
    <div className='user-register-form'>
      <form onSubmit={handleSubmit}>
        <h2>User Registration</h2>
        <div className='mb-3'>
          <label htmlFor="user-name">Name:</label>
          <input
            className='form-control'
            type="text"
            id="user-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
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
        <div className='mb-3'>
          <label htmlFor="user-repassword">Re-Password:</label>
          <input
            className='form-control'
            type="password"
            id="user-repassword"
            value={repassword}
            onChange={(e) => setRePassword(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" type="submit">Register</button>
      </form>
    </div>
  );
};

export default UserRegisterForm;