import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/raw/reviews_with_sentiment.csv')

# Sentiment by bank chart
fig, ax = plt.subplots(figsize=(10, 6))
counts = df.groupby(['bank', 'sentiment_label']).size().unstack()
counts.plot(kind='bar', stacked=True, ax=ax, color=['#ff6b6b', '#95e1d3', '#4ecdc4'])
ax.set_title('Sentiment Distribution by Bank')
ax.set_xlabel('Bank')
ax.set_ylabel('Number of Reviews')
plt.tight_layout()
plt.savefig('reports/sentiment_by_bank.png', dpi=150)
print("Chart saved!")
