# Recommendation System

This project is a recommendation system for movies, built using FastAPI for the backend and React for the frontend. The system allows users to register, log in, and receive movie recommendations based on their preferences. The backend interacts with a SQLite database to store user information, movie data, and preferences. It also supports integrating movie data from IMDb.

## Features

- **User Authentication**: Users can register, log in, and manage their account using JWT authentication.
- **Movie Recommendations**: The system recommends movies based on user preferences (such as genres and ratings) using a collaborative filtering approach.
- **Bulk Movie Import**: Movies can be added to the system through bulk importing from IMDb based on movie titles.
- **Genres Management**: Users can associate movies with multiple genres, and recommendations are influenced by these associations.
- **Frontend and Backend Separation**: A React frontend interacts with a FastAPI backend to provide a smooth user experience.

## Project Structure

The project is divided into two main parts:

### Backend (FastAPI)

- **Backend directory** contains the FastAPI app, which handles the API requests, authentication, and movie recommendations.
- The backend is connected to a SQLite database for persistent storage.
  
### Frontend (React)

- **Frontend directory** contains the React app, which provides the UI for users to interact with the application.
- Users can register, log in, and view recommendations through the React interface.

## Prerequisites

Before running the project, make sure to have the following installed:

- Python 3.8+
- Node.js (with npm or yarn)
- SQLite (or other databases, if you choose to change it)

## Setup Instructions

### Backend Setup

1. **Navigate to the backend directory** and install dependencies:
- `cd backend pip install -r requirements.txt`
3. **Start the FastAPI server**:
- `uvicorn app.main:app --reload`
- The backend will be running at `http://127.0.0.1:8000`.

4. **Create the database and tables**:
The application will automatically create the necessary tables when the FastAPI server is run for the first time.

### Frontend Setup

1. **Navigate to the frontend directory**:
- `cd frontend`
3. **Install dependencies**:
- `npm install`
4. **Start the React development server**:
- `npm start`
- The frontend will be available at `http://localhost:3000`.

### Configuration

The application uses environment variables for configuration. Make sure to set the following in your `.env` file in the backend directory:
- `SECRET_KEY=<your_secret_key> ALGORITHM=HS256 ACCESS_TOKEN_EXPIRES_MINUTES=30`

## API Endpoints

### User Authentication

- **POST /users/register/**: Register a new user.
- **POST /users/login/**: Log in and receive a JWT token.

### Movie Management

- **POST /movies/import/**: Import a movie by title from IMDb.
- **POST /movies/import_bulk/**: Import multiple movies by title from IMDb.
- **POST /movies/**: Add a new movie to the database.
- **POST /users/preferences/**: Add user preference by movie.
- **GET /movies/recommendations/**: Get movie recommendations based on the user's preferences.

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy (ORM), SQLite
- **Frontend**: React, Axios (for making API requests)
- **Authentication**: JWT (JSON Web Tokens)
- **Data Processing**: Pandas, Scikit-learn (for recommendation algorithms)
- **Web Scraping**: IMDb API for fetching movie data

## License

- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

- Feel free to fork this repository, open issues, and submit pull requests. Contributions are welcome!

## Author

- Nikolai Kuznetsov

## Acknowledgments

- Thanks to FastAPI, React, and all the open-source libraries used in this project.
