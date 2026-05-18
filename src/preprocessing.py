"""Separate preprocessing script for review data cleaning."""
import pandas as pd

def preprocess_reviews(input_file='data/raw/reviews.csv', output_file='data/raw/reviews_clean.csv'):
    """Load raw reviews, clean, and save."""
    df = pd.read_csv(input_file)
    initial = len(df)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['review'])
    after_dedup = len(df)
    
    # Remove missing text or rating
    df = df.dropna(subset=['review', 'rating'])
    df = df[df['review'].str.strip() != '']
    final = len(df)
    
    # Normalize dates
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    df.to_csv(output_file, index=False)
    
    print(f"Preprocessing complete: {initial} -> {after_dedup} -> {final}")
    return df

if __name__ == "__main__":
    preprocess_reviews()
