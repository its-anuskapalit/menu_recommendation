import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
import warnings

warnings.filterwarnings('ignore')


class MenuRecommender:
    def __init__(self, data):
        self.data = data
        self.main_items = data[data['category'] == 'main']
        self.side_items = data[data['category'] == 'side']
        self.drink_items = data[data['category'] == 'drink']

    def calculate_combo_score(self, main, side, drink):
        total_calories = main['calories'] + side['calories'] + drink['calories']
        avg_popularity = (main['popularity_score'] + side['popularity_score'] + drink['popularity_score']) / 3
        taste_profiles = {main['taste_profile'], side['taste_profile'], drink['taste_profile']}
        taste_diversity = len(taste_profiles)
        combo_score = avg_popularity * taste_diversity * 0.1 + (1000 - abs(total_calories - 800)) * 0.001

        return {
            'total_calories': total_calories,
            'avg_popularity': avg_popularity,
            'taste_diversity': taste_diversity,
            'combo_score': combo_score
        }

    def generate_all_combos(self):
        combos = []
        for _, main in self.main_items.iterrows():
            for _, side in self.side_items.iterrows():
                for _, drink in self.drink_items.iterrows():
                    combo_info = self.calculate_combo_score(main, side, drink)
                    combos.append({
                        'main': main['item_name'],
                        'main_taste': main['taste_profile'],
                        'main_calories': main['calories'],
                        'main_popularity': main['popularity_score'],
                        'side': side['item_name'],
                        'side_taste': side['taste_profile'],
                        'side_calories': side['calories'],
                        'side_popularity': side['popularity_score'],
                        'drink': drink['item_name'],
                        'drink_taste': drink['taste_profile'],
                        'drink_calories': drink['calories'],
                        'drink_popularity': drink['popularity_score'],
                        'total_calories': combo_info['total_calories'],
                        'avg_popularity': combo_info['avg_popularity'],
                        'taste_diversity': combo_info['taste_diversity'],
                        'combo_score': combo_info['combo_score']
                    })
        return pd.DataFrame(combos)

    def recommend_3_day_menu(self, calorie_range=(700, 900), min_popularity=0.7, ensure_diversity=True):
        all_combos = self.generate_all_combos()
        filtered = all_combos[
            (all_combos['total_calories'] >= calorie_range[0]) &
            (all_combos['total_calories'] <= calorie_range[1]) &
            (all_combos['avg_popularity'] >= min_popularity)
        ].copy()

        if len(filtered) < 3:
            filtered = all_combos.nlargest(10, 'combo_score')
        filtered = filtered.sort_values('combo_score', ascending=False)
        selected, used_items = [], set()
        for _, combo in filtered.iterrows():
            items = {combo['main'], combo['side'], combo['drink']}
            if ensure_diversity and items & used_items:
                continue
            selected.append(combo)
            used_items |= items
            if len(selected) == 3:
                break
        while len(selected) < 3 and len(filtered) > len(selected):
            combo = filtered.iloc[len(selected)]
            selected.append(combo)
        return selected
        
    def display_recommendations(self, recommendations):
        total_calories = []
        total_popularity = []
        for i, combo in enumerate(recommendations, 1):
            print(f"\nDAY {i}")
            print("-" * 40)
            print(f"MAIN : {combo['main']} ({combo['main_taste']}) - {combo['main_calories']} cal")
            print(f"SIDE : {combo['side']} ({combo['side_taste']}) - {combo['side_calories']} cal")
            print(f"DRINK: {combo['drink']} ({combo['drink_taste']}) - {combo['drink_calories']} cal")
            print(f"TOTAL CALORIES: {combo['total_calories']}")
            print(f"AVG POPULARITY: {combo['avg_popularity']:.2f}")
            print(f"TASTE DIVERSITY: {combo['taste_diversity']}")
            print(f"COMBO SCORE: {combo['combo_score']:.3f}")

            total_calories.append(combo['total_calories'])
            total_popularity.append(combo['avg_popularity'])
        print(f"\nCALORIE RANGE: {min(total_calories)} - {max(total_calories)}")
        print(f"AVG CALORIES : {np.mean(total_calories):.0f}")
        print(f"POPULARITY RANGE: {min(total_popularity):.2f} - {max(total_popularity):.2f}")
        print(f"AVG POPULARITY  : {np.mean(total_popularity):.2f}")
        return pd.DataFrame(recommendations)

    def plot_analysis(self):
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Menu Dataset Analysis', fontsize=16, fontweight='bold')

        cat_calories = self.data.groupby('category')['calories'].mean()
        axes[0, 0].bar(cat_calories.index, cat_calories.values, color=['skyblue', 'lightgreen', 'lightcoral'])
        axes[0, 0].set_title('Average Calories by Category')

        axes[0, 1].hist(self.data['popularity_score'], bins=10, color='gold', alpha=0.7)
        axes[0, 1].set_title('Popularity Score Distribution')

        taste_counts = self.data['taste_profile'].value_counts()
        axes[1, 0].bar(taste_counts.index, taste_counts.values, color=['orange', 'purple', 'green'])
        axes[1, 0].set_title('Taste Profile Distribution')

        colors = {'main': 'red', 'side': 'blue', 'drink': 'green'}
        for category in self.data['category'].unique():
            d = self.data[self.data['category'] == category]
            axes[1, 1].scatter(d['calories'], d['popularity_score'],
                              c=colors[category], label=category, alpha=0.7, s=60)

        axes[1, 1].set_title('Calories vs Popularity by Category')
        axes[1, 1].legend()
        plt.tight_layout()
        plt.show()


def load_menu_data():
    data = {
        'item_name': [
            'Paneer Butter Masala', 'Chicken Biryani', 'Vegetable Pulao', 'Rajma Chawal',
            'Chole Bhature', 'Masala Dosa', 'Grilled Sandwich', 'Garlic Naan', 'Mixed Veg Salad',
            'French Fries', 'Curd Rice', 'Papad', 'Paneer Tikka', 'Masala Chaas', 'Sweet Lassi',
            'Lemon Soda', 'Cold Coffee', 'Coconut Water', 'Iced Tea'
        ],
        'category': [
            'main', 'main', 'main', 'main', 'main', 'main', 'main',
            'side', 'side', 'side', 'side', 'side', 'side',
            'drink', 'drink', 'drink', 'drink', 'drink', 'drink'
        ],
        'calories': [
            450, 600, 400, 500, 650, 480, 370,
            200, 150, 350, 250, 100, 300,
            100, 220, 90, 180, 60, 120
        ],
        'taste_profile': [
            'spicy', 'spicy', 'savory', 'savory', 'spicy', 'savory', 'savory',
            'savory', 'sweet', 'savory', 'savory', 'savory', 'spicy',
            'spicy', 'sweet', 'savory', 'sweet', 'sweet', 'sweet'
        ],
        'popularity_score': [
            0.9, 0.95, 0.7, 0.8, 0.85, 0.88, 0.6,
            0.9, 0.75, 0.8, 0.7, 0.65, 0.85,
            0.8, 0.9, 0.7, 0.75, 0.6, 0.78
        ]
    }
    return pd.DataFrame(data)
