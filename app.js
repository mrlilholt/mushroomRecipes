import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [mushroom, setMushroom] = useState('');
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchRecipes = async () => {
    if (!mushroom) return;
    setLoading(true);
    setError('');
    setRecipes([]);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/search?mushroom=${mushroom}`);
      setRecipes(response.data);
    } catch (err) {
      console.error('Error fetching recipes:', err);
      setError('Failed to fetch recipes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Mushroom Recipe Finder</h1>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Enter mushroom type (e.g., chanterelle)"
          value={mushroom}
          onChange={(e) => setMushroom(e.target.value)}
        />
        <button onClick={fetchRecipes}>Search</button>
      </div>

      {loading && <p>Loading recipes...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div className="recipe-grid">
        {recipes.map((recipe, index) => (
          <div key={index} className="recipe-card">
            <img src={recipe.image_url} alt={recipe.title} />
            <h3>{recipe.title}</h3>
            <p>⭐ {recipe.rating} stars ({recipe.ratings_count} reviews)</p>
            <a href={recipe.link} target="_blank" rel="noopener noreferrer">View Recipe</a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
