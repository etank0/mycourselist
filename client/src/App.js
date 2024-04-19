import './App.css';
import Navbar from './Components/Navbar';
import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes,Route, Navigate } from "react-router-dom";
import UserLoginForm from './Components/Forms/UserLoginForm';
import AdminLoginForm from './Components/Forms/AdminLoginForm';
import UserRegisterForm from './Components/Forms/UserRegisterForm';
import LandingPage from './Pages/LandingPage';
import HomePage from './Pages/HomePage';
import 'bootstrap/dist/css/bootstrap.min.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import UserCatalog from './Pages/UserCatalog';
import AdminCourseForm from './Components/Forms/AdminCourseForm';
import CourseList from './Pages/CourseList'

function App() {
  const [user, setUser] = useState(null);

  // Fetch user data from localStorage when the component mounts
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []); // Empty dependency array ensures this effect runs only once on mount

  return (
    <div className="App">
      <Router>
        <Navbar user={user}/>
        <Routes>
            <Route path='/' element={user ? <Navigate to="/home" /> : <LandingPage />} />
            <Route path='/home' element={user ? <HomePage user={user} /> : <Navigate to="/" />} />
            <Route path='/user/login' element={user ? <Navigate to="/home" /> : <UserLoginForm />} />
            <Route path='/admin/login' element={user ? <Navigate to="/home" /> : <AdminLoginForm />} />
            <Route path='/user/register' element={user ? <Navigate to="/home" /> : <UserRegisterForm />} />
            <Route path='/user/catalog' element={user ? <UserCatalog user={user}/> : <Navigate to="/home" />} />
            <Route path='/admin/add' element={user ? <AdminCourseForm /> : <Navigate to="/home" />} />
            <Route path="/users/:username" element={<CourseList />} />
        </Routes>
      </Router>
      <ToastContainer />
    </div>
  );
}

export default App;
