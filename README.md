# 🎬 Movie Recommendation System

A simple yet powerful content-based Movie Recommendation System built with **Streamlit**. It allows users to pick a movie and get instant recommendations based on similarity.

---

## 🚀 Features

- ✅ Select a movie from dropdown menu
- ✅ Instantly see top 5 similar movies with their posters
- ✅ Uses precomputed similarity matrix for fast recommendations
- ✅ Live poster fetching using **TMDb API**
- ✅ Fully deployable on Streamlit Cloud

---

## 🛠️ Tech Stack

- Python 3
- Streamlit
- Pandas
- Scikit-learn
- TMDb API (for fetching movie posters)

---

## 🌐 Live Demo

👉 [Click here to try the app](https://movie-recommendation-system-by-ishanjain.streamlit.app/)



---

## 📦 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/jnishanjain/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Get your TMDb API Key

- Create a free account at [TMDb](https://www.themoviedb.org/documentation/api)
- Generate an API key
- Open `app.py` and replace the existing API key with your own:

```python
url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
```

### 4️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

---

## 🖼️ Screenshot



*(Add a screenshot image of your app UI here)*

---

## 📄 License

This project is licensed under the MIT License.

---

Made with ❤️ using Streamlit.

