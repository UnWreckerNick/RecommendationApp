import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
          setError('No token found');
          return;
        }

        const response = await axios.get('http://127.0.0.1:8000/movies/recommendations/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setRecommendations(response.data);
      } catch (err) {
        setError('Error fetching recommendations');
        console.error(err);
      }
    };

    fetchRecommendations();
  }, []);

  return (
    <div>
      <h2>Recommendations</h2>
      {error && <p>{error}</p>}
      {recommendations.length > 0 ? (
        <ul>
          {recommendations.map((movie) => (
            <li key={movie.id}>{movie.title} - {movie.similarity}</li>
          ))}
        </ul>
      ) : (
        <p>No recommendations available</p>
      )}
    </div>
  );
};

export default Recommendations;
