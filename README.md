# 🎬 Movie Recommendation System

An interactive **content-based movie recommendation system** built with **Python**, **Streamlit**, and **scikit-learn**.
It uses **cosine similarity** to recommend movies similar to a selected title and fetches extra details (plot, cast, ratings, and posters) using **TMDb** and **OMDb** APIs.

---

## 📌 Features

* **Movie Search:** Select any movie from the list to get recommendations
* **Top 5 Similar Movies:** Based on cosine similarity of content features
* **Extra Info:** Movie poster, plot summary, cast, and rating displayed
* **Live API Integration:** Fetches real-time details from TMDb & OMDb
* **Clean UI:** Styled with custom CSS for a modern feel and background image

---

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit** – Web app framework
* **Pandas** – Data manipulation
* **scikit-learn** – Vectorization & cosine similarity
* **Joblib** – Model/data loading
* **Requests** – API calls to TMDb & OMDb

---

## 📂 Dataset

* Movies dataset processed & stored in `movies.pkl`
* Similarity matrix precomputed and stored in `similarity.pkl`
* Original source: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

## 🚀 Installation & Setup

```bash
# Clone this repository
git clone https://github.com/your-username/movie-recommendation-system.git

# Navigate into the project folder
cd movie-recommendation-system

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---

## 🔑 API Keys Required

This app uses:

* **TMDb API** → [Get API Key](https://developer.themoviedb.org/docs)
* **OMDb API** → [Get API Key](https://www.omdbapi.com/apikey.aspx)

Replace placeholders in `app.py`:

```python
OMDB_API_KEY = 'your_omdb_api_key'
API_KEY = 'your_tmdb_api_key'
```

---

## 📸 Screenshots

(Add your app screenshots here)

---

## 💡 How It Works

1. Load preprocessed movie dataset & cosine similarity matrix (`movies.pkl`, `similarity.pkl`)
2. On movie selection, compute similarity scores and return top 5 similar movies
3. Fetch posters, plot, cast, and ratings from TMDb & OMDb APIs
4. Display recommendations in a visually appealing card layout

---

## 👨‍💻 Author

**Afshal Liaquat**
* LinkedIn: [Afshal Liaquat](https://www.linkedin.com/in/afshal-liaquat-972196205/)
