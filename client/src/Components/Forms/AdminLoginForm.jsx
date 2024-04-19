import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./AdminLoginForm.css";
import { toast } from 'react-toastify'; 

const AdminLoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const response = await axios.post('http://localhost:4000/admin/login', {
          username,
          password
        });
        
        const { data } = response;
        data.admin.isAdmin = true;

        console.log(data.admin);
        
        // Store data in localStorage
        localStorage.setItem('user', JSON.stringify(data.admin));
        toast.success("Login Successful!");
        console.log('Admin login successful');
        console.log(JSON.parse(localStorage.getItem('user')));
        navigate("/home");
    } catch (error) {
        console.error('Admin login failed:', error);
        toast.success("Login Failed!");
    }

    // Reset form fields
    setUsername('');
    setPassword('');
  };

  return (
    <div className='admin-login-form'>
      <form onSubmit={handleSubmit}>
        <h2>Admin Login</h2>
        <div className='mb-3'>
          <label className="form-label" htmlFor="admin-username">Username:</label>
          <input
            className='form-control'
            type="text"
            id="admin-username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className='mb-3'>
          <label htmlFor="admin-password">Password:</label>
          <input
            className='form-control'
            type="password"
            id="admin-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" type="submit">Login</button>
      </form>
    </div>
  );
};

export default AdminLoginForm;