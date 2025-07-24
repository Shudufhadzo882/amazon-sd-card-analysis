# amazon_review_cleaner.py
import pandas as pd

# Read raw data
df = pd.read_csv('amazon_reviews.csv', header=None)
df.columns = ['review_id', 'reviewer', 'rating', 'review_text', 'review_date', 'helpful_votes', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6']
df = df[['review_id', 'reviewer', 'rating', 'review_text', 'review_date', 'helpful_votes']]

# Extract device
def extract_device(text):
    devices = ['Galaxy S4', 'Note 2', 'GoPro', 'Surface', 'LG Optimus', 'BlackBerry']
    for d in devices:
        if d.lower() in str(text).lower():
            return d
    return "Other"
df['device_used'] = df['review_text'].apply(extract_device)

# Extract storage size
import re
df['storage_size_gb'] = df['review_text'].apply(lambda x: int(re.search(r'(\d+)\s*GB', str(x), re.IGNORECASE).group(1)) if re.search(r'(\d+)\s*GB', str(x), re.IGNORECASE) else 32)

# Sentiment (simple)
df['sentiment'] = df['review_text'].apply(lambda x: 'Positive' if 'great' in str(x).lower() or 'good' in str(x).lower() else 'Neutral')

# Clean date
df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')

# Add length
df['review_length'] = df['review_text'].astype(str).apply(len)

# Save
df.to_csv('cleaned_amazon_sdcard_reviews.csv', index=False)
print("✅ Cleaned file saved!")
