import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Recommendations from './Recommendations';

function App() {
  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/users/login">Login</Link></li>
          <li><Link to="/users/register">Register</Link></li>
          <li><Link to="/movies/recommendations/">Recommendations</Link></li>
        </ul>
      </nav>

      <Routes>
        <Route path="/users/login" element={<Login />} />
        <Route path="/users/register" element={<Register />} />
        <Route path="/movies/recommendations/" element={<Recommendations />} />
        <Route path="/" element={<h1>Welcome to Recommendation App</h1>} />
      </Routes>
    </Router>
  );
}


export default App;
