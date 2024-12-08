import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [token, setToken] = useState('');

    const handleLogin = async () => {
        setLoading(true);
        setErrorMessage('');
        setSuccessMessage('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/users/login/', {
                username,
                password
            });
            
            const { access_token } = response.data;
            setToken(access_token);
            setSuccessMessage('Login successful!');
        } catch (error) {
            setErrorMessage('Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            <button onClick={handleLogin} disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
            </button>

            {errorMessage && <div className="error-popup">{errorMessage}</div>}

            {successMessage && <div className="success-popup">{successMessage}</div>}
        </div>
    );
};

export default Login;
