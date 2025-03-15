# Personalized Netflix Content Recommender

![Netflix Logo](https://upload.wikimedia.org/wikipedia/commons/7/7a/Logonetflix.png)

Welcome to the **Personalized Netflix Content Recommender**! This project is designed to provide personalized movie and TV show recommendations based on user preferences and viewing history. It integrates with **The Movie Database (TMDB)** to fetch movie posters and details, and it uses a collaborative filtering approach to generate recommendations.

---

## Features

- **User Authentication**: Secure login and registration system.
- **Personalized Recommendations**: Get movie recommendations based on your preferences and viewing history.
- **Watchlist Management**: Add movies to your watchlist and mark them as watched.
- **Watched History**: Keep track of the movies you've watched.
- **Interactive UI**: User-friendly interface built with **Streamlit**.
- **TMDB Integration**: Fetch movie posters and details from TMDB.

---
## Project structure
    ```bash
    Personalized-Netflix-Content-Recommender/
    │
    ├── app/
    │   ├── auth/
    │   │   ├── __init__.py
    │   │   ├── components.py
    │   │   ├── database.py
    │   │   └── users.py
    │   ├── data_manager.py
    │   ├── poster_utils.py
    │   ├── recommender.py
    │   ├── ui_components.py
    │   └── main.py
    │
    ├── data/
    │   ├── movies_df.csv
    │   └── movies_sim.npz
    │
    ├── assets/
    │   └── default_poster.png
    │
    ├── .env
    ├── requirements.txt
    └── README.md


---

## How It Works

1. **User Authentication**:
   - Users can register and log in to the system.
   - Authentication is handled securely using **bcrypt** for password hashing.

2. **Movie Recommendations**:
   - Users can search for movies and get personalized recommendations.
   - Recommendations are generated using a **collaborative filtering** approach based on user preferences and viewing history.

3. **Watchlist and Watched Movies**:
   - Users can add movies to their watchlist and mark them as watched.
   - The system keeps track of the user's watchlist and watched movies.

4. **TMDB Integration**:
   - Movie posters and details are fetched from **The Movie Database (TMDB)** API.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Streamlit
- MongoDB (for user data storage)
- TMDB API key

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mannemkarthik010/Personalized-Netflix-Content-Recommender.git
   cd Personalized-Netflix-Content-Recommender
2. **Set Up Environment Variables:**:
   * Create a .env file in the root directory and add the following variables:
   ```bash
   MONGO_URI=your_mongodb_connection_string
   DB_NAME=your_database_name
   TMDB_API_KEY=your_tmdb_api_key
3. **Run the Application:**
   ```bash
   streamlit run main.py
4. **Access the Application:**
   * Open your browser and go to http://localhost:8501.




## Technologies Used

* Python: Core programming language.
* Streamlit: For building the interactive web interface.
* MongoDB: For storing user data (watchlist, watched movies, etc.).
* TMDB API: For fetching movie posters and details.
* Pandas & NumPy: For data manipulation and recommendation algorithms.

## Screenshots

**Homepage**

<img width="1440" alt="Screenshot 2025-03-14 at 9 52 25 PM" src="https://github.com/user-attachments/assets/c7f43064-6e3b-4d76-a0c9-3247cf16dea5" />

**Recommendations Page**

<img width="1440" alt="Screenshot 2025-03-14 at 9 52 38 PM" src="https://github.com/user-attachments/assets/27fdb3cc-b5e1-4ec3-afa3-0ddc8ce45462" />

**Watchlist Page**

<img width="1440" alt="Screenshot 2025-03-14 at 9 52 48 PM" src="https://github.com/user-attachments/assets/7caf0199-4f6a-49c8-b02e-004284e641a3" />

**Watched Movies Page**

<img width="1440" alt="Screenshot 2025-03-14 at 9 52 59 PM" src="https://github.com/user-attachments/assets/519c3998-8b44-4515-8634-25f4a9b57834" />



## Contributions
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (git checkout -b feature/YourFeatureName).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeatureName).
5. Open a pull request.

## Acknowledgments
* The Movie Database (TMDB): For providing movie data and posters.
* Streamlit: For making it easy to build interactive web apps.
* MongoDB: For providing a flexible NoSQL database solution.

  
