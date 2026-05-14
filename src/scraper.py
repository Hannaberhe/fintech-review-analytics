from google_play_scraper import reviews, Sort, search
import pandas as pd

APPS = {
    'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
    'Dashen Bank': 'com.dashen.dashensuperapp',
    'Bank of Abyssinia': 'africa.of.boamobile'
}

def get_app_id(bank_name):
    """Get app ID - use known ID or search"""
    if bank_name in APPS:
        return APPS[bank_name]
    
    # Try searching
    try:
        results = search(bank_name, n_hits=3, country='et')
        for r in results:
            if r['appId'] and ('bank' in r['title'].lower() or 'boa' in r['title'].lower()):
                return r['appId']
    except:
        pass
    
    return None

def scrape_reviews(app_id, app_name, count=500):
    """Scrape reviews for a given app."""
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=count
        )
        
        data = []
        for review in result:
            data.append({
                'review': review['content'],
                'rating': review['score'],
                'date': review['at'].strftime('%Y-%m-%d'),
                'bank': app_name,
                'source': 'Google Play'
            })
        
        print(f"  Got {len(data)} reviews")
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"  Error: {e}")
        # Try with empty dataframe
        return pd.DataFrame()

if __name__ == "__main__":
    banks = ['Commercial Bank of Ethiopia', 'Dashen Bank', 'Bank of Abyssinia']
    all_data = []
    
    for bank in banks:
        print(f"\n{'='*50}")
        print(f"Scraping: {bank}")
        print(f"{'='*50}")
        
        app_id = get_app_id(bank)
        if app_id:
            print(f"  App ID: {app_id}")
            df = scrape_reviews(app_id, bank, 500)
            all_data.append(df)
        else:
            print(f"  Could not find app ID for {bank}")
    
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal before cleaning: {len(df)}")
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['review'])
        
        # Remove empty reviews
        df = df.dropna(subset=['review', 'rating'])
        df = df[df['review'].str.strip() != '']
        
        df.to_csv('data/raw/reviews.csv', index=False)
        
        print(f"Total after cleaning: {len(df)}")
        print(f"\nReviews per bank:")
        print(df['bank'].value_counts())
    else:
        print("\nNo reviews collected!")