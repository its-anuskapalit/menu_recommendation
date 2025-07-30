# 🍽️ AI-Based Menu Recommender System

A personalized 3-day meal planner that leverages AI to recommend food combos based on user-selected taste profiles, calorie preferences, and popularity scores. Built using **Streamlit**, **Pandas**, and **custom recommendation logic**, this project makes meal planning smart, diverse, and user-centric.

---

## 🔍 Features

- 🎯 **3-Day Personalized Menu Planning**
  - Based on user's preferred taste for Day 1 (e.g., spicy, sweet, savory)
  - Ensures diversity in taste and food items across all days
  - Calorie and popularity filtering to match dietary goals

- 📊 **Combo Scoring Algorithm**
  - Calculates total calories, average popularity, and taste diversity
  - Ranks combinations using a custom scoring formula

- 🧠 **Interactive Web App**
  - Built with Streamlit for real-time, browser-based usage
  - Sliders and dropdowns to control filters and preferences

- 📈 **Analytics & Visualization**
  - Optional dataset and combo analysis using matplotlib/seaborn

---

## 🗂️ Project Structure

```bash
├── app.py                  # Streamlit frontend app
├── model.py                # Recommender logic + combo scoring
├── menu_recommender.py     # Alternative module with additional plots & debug output
├── menu.ipynb              # Data exploration and visual analysis
├── recommendation.ipynb    # Optional Jupyter notebook for recommendation outputs
├── AI Menu Recommender Items.csv  # Sample dataset (if not loaded programmatically)
├── sample_output.json      # Example recommendations in JSON format
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-menu-recommender.git
cd ai-menu-recommender
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Example dependencies:
> ```
> streamlit
> pandas
> matplotlib
> seaborn
> ```

### 3. Run the Web App

```bash
streamlit run app.py
```

### 4. Use the App

- Select your starting day.
- Choose your taste profile for Day 1.
- Adjust calorie and popularity preferences.
- Click “🎯 Recommend 3-Day Plan” to view results.

---

## 📦 Dataset Overview

The menu dataset includes:

- Categories: `main`, `side`, `drink`
- Taste profiles: `spicy`, `savory`, `sweet`
- Nutritional data: Calories
- Popularity scores (0–1 scale)

---

## 🧠 Recommendation Logic

The combo scoring formula is:

```
combo_score = (average_popularity × taste_diversity × 0.1) + (1000 - |total_calories - 800|) × 0.001
```

This rewards:
- High popularity
- Diverse taste combinations
- Calorie targets near 800 kcal

---

## 📌 Example Output

```json
[
  {
    "combo_id": 1,
    "main": "Chicken Biryani",
    "side": "Garlic Naan",
    "drink": "Masala Chaas",
    "total_calories": 750,
    "popularity_score": 2.4,
    "reasoning": "Spicy profile fits Friday trends, popular choices, calorie target met"
  }
]
```

---

## ✨ Screenshots

_Add screenshots of your Streamlit app interface here._

---

## 👩‍💻 Author

- **Anuska Palit**
- Cloud & ML enthusiast | Final-year CS student at LPU

---

## 📃 License

This project is open source and available under the [MIT License](LICENSE).
