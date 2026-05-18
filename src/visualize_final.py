import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/raw/reviews_with_sentiment.csv')

# Chart 1: Rating distribution by bank
fig, ax = plt.subplots(figsize=(10, 6))
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    ax.hist(bank_df['rating'], alpha=0.5, label=bank, bins=5)
ax.set_title('Rating Distribution by Bank')
ax.set_xlabel('Star Rating')
ax.set_ylabel('Number of Reviews')
ax.legend()
plt.tight_layout()
plt.savefig('reports/rating_distribution.png', dpi=150)
print("Chart 1 saved!")

# Chart 2: Theme frequency by bank
fig, ax = plt.subplots(figsize=(12, 6))
theme_counts = df.groupby(['bank', 'theme']).size().unstack().fillna(0)
theme_counts.plot(kind='bar', ax=ax)
ax.set_title('Theme Frequency by Bank')
ax.set_xlabel('Bank')
ax.set_ylabel('Number of Reviews')
ax.legend(title='Theme', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('reports/theme_frequency.png', dpi=150)
print("Chart 2 saved!")

# Chart 3: Average rating by theme
fig, ax = plt.subplots(figsize=(10, 6))
avg_rating = df.groupby('theme')['rating'].mean().sort_values()
avg_rating.plot(kind='barh', ax=ax, color='steelblue')
ax.set_title('Average Rating by Theme')
ax.set_xlabel('Average Rating')
plt.tight_layout()
plt.savefig('reports/rating_by_theme.png', dpi=150)
print("Chart 3 saved!")

# Chart 4: Sentiment score distribution
fig, ax = plt.subplots(figsize=(10, 6))
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    ax.hist(bank_df['sentiment_score'], alpha=0.5, label=bank, bins=20)
ax.set_title('Sentiment Score Distribution by Bank')
ax.set_xlabel('Sentiment Score')
ax.set_ylabel('Number of Reviews')
ax.legend()
plt.tight_layout()
plt.savefig('reports/sentiment_distribution.png', dpi=150)
print("Chart 4 saved!")

print("\nAll charts saved in reports/")
