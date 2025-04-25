# Movie Recommendation System

This project implements a movie recommendation system using Python, Streamlit, and a machine learning model.

## Files

* `app.py`:  The Streamlit application for interacting with the recommendation system.
* `Recommendation System.ipynb`: Jupyter Notebook used to build and train the movie recommendation model.
* `movies.pkl`:  Preprocessed movie data.
* `similarity.pkl`:  Similarity matrix used for recommendations.
* `data/tmdb_5000_movies.csv`:  Raw movie dataset.
* `data/tmdb_5000_credits.csv`: Raw credits dataset.
* `requirements.txt`:  List of Python dependencies.

## Setup

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/Movie-Recommendation-System.git](https://github.com/jnishanjain/Movie-Recommendation-System.git)
    cd Movie-Recommendation-System
    ```
2.  (Optional) Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Streamlit App

```bash
streamlit run app.py
