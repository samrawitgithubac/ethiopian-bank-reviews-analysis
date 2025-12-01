from google_play_scraper import reviews, Sort
import pandas as pd
from dateutil import parser
import time

APPS = {
    "CBE": "com.cbe.eBanking",
    "BOA": "com.ambel.mobile.android",
    "Dashen": "com.dashenbank.mwallet"
}

def scrape_bank_reviews(bank_name, app_id, total=400):
    print(f"\nScraping {bank_name}...")
    all_reviews = []
    count = 0
    next_token = None

    while count < total:
        result, next_token = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=200,
            continuation_token=next_token
        )

        all_reviews.extend(result)
        count += len(result)
        print(f"Collected {count} reviews so far...")
        time.sleep(1)

        if not next_token:
            break

    df = pd.DataFrame(all_reviews)
    df["bank"] = bank_name
    df["source"] = "Google Play"
    return df

dfs = []
for bank, app_id in APPS.items():
    df_bank = scrape_bank_reviews(bank, app_id)
    dfs.append(df_bank)

df_all = pd.concat(dfs, ignore_index=True)

# Keep only relevant columns
df_clean = df_all[["content", "score", "at", "bank", "source"]]
df_clean.rename(columns={
    "content": "review",
    "score": "rating",
    "at": "date"
}, inplace=True)

# Normalize date format
df_clean["date"] = df_clean["date"].apply(lambda d: d.strftime("%Y-%m-%d") if pd.notnull(d) else None)

# Remove duplicates + missing
df_clean.drop_duplicates(subset=["review"], inplace=True)
df_clean.dropna(subset=["review", "rating"], inplace=True)

# Save
df_clean.to_csv("bank_reviews_clean.csv", index=False)

print("\nScraping completed! File saved as bank_reviews_clean.csv")
