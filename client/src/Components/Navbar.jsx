import './Navbar.css';
import navlogo from '../newnavbar.png';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const NavList = (props) => {
    const { user } = props;
    
    return (
        user.isAdmin ? 
        <>
            <Link to="/admin/add" className="btn btn-primary">
                Add Course
            </Link>
        </>
        :
        <>
            <Link to="/user/catalog" className="btn btn-primary">
                Catalog
            </Link>
        </>
    )
}

const Navbar = (props) => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        localStorage.removeItem('user');
        
        toast.success("Logged Out!");
        navigate("/");
    }
    const { user } = props;
    return (
        <div className="nav-container">
            <div className="nav-logo">
                <div className="logo-container">
                    <Link to="/">
                        <img src={navlogo} alt="logo" />
                    </Link>
                </div>
            </div>
            <div className="nav-list">
                    <Link to="/" className="btn btn-primary">
                        Home
                    </Link>
                    {
                        user ? 
                        <NavList user={user}/> :
                        <></>
                    }
                    {
                        user ?
                        <Link className='btn btn-danger' onClick={handleLogout}>Logout</Link>
                        : <></>
                    }
            </div>
        </div>
    )
}

export default Navbar;