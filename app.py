import streamlit as st
import pandas as pd
from model import MenuRecommender, load_menu_data

st.set_page_config(page_title="Restaurants  Taste-Based Menu Planner", layout="centered")

st.markdown("<h1 style='text-align:center; color:#FF5722;'>🍽️ Personalized 3-Day Menu Plan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Start with your favorite taste and let ai generate a smart 3-day meal journey 🍛🥗🥤</p>", unsafe_allow_html=True)

df = load_menu_data()
recommender = MenuRecommender(df)

# Sidebar filters
st.sidebar.header("Plan Configuration")
start_day = st.sidebar.selectbox("Choose starting day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
available_tastes = df['taste_profile'].unique().tolist()
preferred_taste = st.sidebar.selectbox("Preferred taste profile for Day 1", available_tastes)
min_cal = st.sidebar.slider("Minimum Calories", 500, 1000, 700)
max_cal = st.sidebar.slider("Maximum Calories", 600, 1200, 900)
min_pop = st.sidebar.slider("Minimum Popularity", 0.0, 1.0, 0.7)

# Combo logic
def generate_flexible_combo(recommender, preferred_taste, calorie_range, min_popularity):
    all_combos = recommender.generate_all_combos()
    combos = all_combos[
        (all_combos['total_calories'] >= calorie_range[0]) &
        (all_combos['total_calories'] <= calorie_range[1]) &
        (all_combos['avg_popularity'] >= min_popularity)
    ].copy()

    if len(combos) < 10:
        combos = all_combos.nlargest(30, 'combo_score')
    
    combos = combos.sort_values("combo_score", ascending=False)
    selected = []
    used_items = set()
    used_tastes = set()

    # Day 1 → must match taste
    for _, row in combos.iterrows():
        if preferred_taste in {row['main_taste'], row['side_taste'], row['drink_taste']}:
            items = {row['main'], row['side'], row['drink']}
            if not used_items.intersection(items):
                selected.append(row)
                used_items.update(items)
                used_tastes.update([row['main_taste'], row['side_taste'], row['drink_taste']])
                break

    # Day 2 and 3 → must have different tastes
    for _, row in combos.iterrows():
        if len(selected) >= 3:
            break
        items = {row['main'], row['side'], row['drink']}
        tastes = {row['main_taste'], row['side_taste'], row['drink_taste']}
        if not used_items.intersection(items) and not tastes.intersection(used_tastes):
            selected.append(row)
            used_items.update(items)
            used_tastes.update(tastes)

    # Fill remaining if necessary (with less strict taste condition)
    for _, row in combos.iterrows():
        if len(selected) >= 3:
            break
        items = {row['main'], row['side'], row['drink']}
        if not used_items.intersection(items):
            selected.append(row)
            used_items.update(items)

    return selected[:3]

# Recommend button
if st.button("🎯 Recommend 3-Day Plan"):
    with st.spinner("Analyzing menus..."):
        final_combos = generate_flexible_combo(
            recommender,
            preferred_taste,
            (min_cal, max_cal),
            min_pop
        )

    if len(final_combos) < 3:
        st.error(" Could not generate 3 unique combos even after fallback. Please change your taste or relax filters.")
    else:
        st.success("Your customized 3-day menu is ready!")

        plan_days = [start_day]
        all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        start_idx = all_days.index(start_day)
        for i in range(1, 3):
            plan_days.append(all_days[(start_idx + i) % 7])

        for i, combo in enumerate(final_combos):
            st.markdown(f"<h3 style='color:#4CAF50;'>📅 {plan_days[i]}</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### 🍛 Main")
                st.write(f"**{combo['main']}**")
                st.write(f"Taste: `{combo['main_taste']}`")
                st.write(f"Calories: `{combo['main_calories']}`")

            with col2:
                st.markdown("#### 🥗 Side")
                st.write(f"**{combo['side']}**")
                st.write(f"Taste: `{combo['side_taste']}`")
                st.write(f"Calories: `{combo['side_calories']}`")

            with col3:
                st.markdown("#### 🥤 Drink")
                st.write(f"**{combo['drink']}**")
                st.write(f"Taste: `{combo['drink_taste']}`")
                st.write(f"Calories: `{combo['drink_calories']}`")

            st.markdown(f"""---
            📊 Summary  
            🔥 Calories: `{combo['total_calories']}`  
            ⭐ Popularity: `{combo['avg_popularity']:.2f}`  
            🎨 Taste Diversity: `{combo['taste_diversity']}`  
            🏆 Combo Score: `{combo['combo_score']:.3f}`
            """)
