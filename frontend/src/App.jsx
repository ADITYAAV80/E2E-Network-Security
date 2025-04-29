/* eslint-disable */
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import Login from './pages/Login';
import DeveloperDashboard from './pages/DeveloperDashboard';
import CustomerDashboard from './pages/CustomerDashboard';
import PrivateRoute from './pages/PrivateRoute';
import Home from './pages/Home';
import Signup from './pages/Signup'; // Assuming you have a signup page

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/developer" element={<PrivateRoute element={<DeveloperDashboard />} role="developer" redirectTo="/login" />} />
        <Route path="/customer" element={<PrivateRoute element={<CustomerDashboard />} role="customer" redirectTo="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;


