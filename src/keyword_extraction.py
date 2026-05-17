"""TF-IDF keyword extraction for thematic analysis."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

def extract_keywords_tfidf(df, bank_name=None, n_keywords=20):
    """Extract top keywords using TF-IDF."""
    if bank_name:
        texts = df[df['bank'] == bank_name]['review']
    else:
        texts = df['review']
    
    stop_words = list(stopwords.words('english'))
    
    vectorizer = TfidfVectorizer(
        max_features=500,
        stop_words=stop_words,
        ngram_range=(1, 2)
    )
    
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    
    # Get top keywords
    top_indices = scores.argsort()[-n_keywords:][::-1]
    keywords = [(feature_names[i], scores[i]) for i in top_indices]
    
    return keywords

if __name__ == "__main__":
    df = pd.read_csv('data/raw/reviews_with_sentiment.csv')
    
    print("Top keywords per bank:")
    for bank in df['bank'].unique():
        print(f"\n{bank}:")
        keywords = extract_keywords_tfidf(df, bank, 10)
        for word, score in keywords:
            print(f"  {word}: {score:.3f}")
    
    # Save keywords
    with open('data/keywords.txt', 'w') as f:
        for bank in df['bank'].unique():
            f.write(f"\n{bank}:\n")
            keywords = extract_keywords_tfidf(df, bank, 10)
            for word, score in keywords:
                f.write(f"  {word}: {score:.3f}\n")
    
    print("\nKeywords saved to data/keywords.txt")
    print("Reviews processed: " + str(len(df)))
