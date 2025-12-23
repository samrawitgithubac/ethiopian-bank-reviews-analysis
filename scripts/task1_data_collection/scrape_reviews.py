from google_play_scraper import reviews, Sort, app
import pandas as pd
import time
import os

# App IDs - Updated based on Google Play Store search results
# Verified using find_app_id.py helper script
APPS = {
    "CBE": ["com.combanketh.mobilebanking", "com.cbe.eBanking"],  # Commercial Bank of Ethiopia Mobile Banking
    "BOA": ["com.boa.boaMobileBanking", "com.ambel.mobile.android"],  # BoA Mobile (Bank of Abyssinia) - Verified: 1M+ installs
    "Dashen": ["com.cr2.amolelight", "com.dashen.mobilebanking", "com.dashenbank.mwallet"]  # Dashen Mobile
}

def scrape_bank_reviews(bank_name, app_id, total=400):
    print(f"\n🔍 Scraping {bank_name} (App ID: {app_id})...")

    all_reviews = []
    token = None
    batch_size = 200  # Increased batch size
    attempts = 0
    max_attempts = 10

    while len(all_reviews) < total and attempts < max_attempts:
        try:
            # First call without continuation_token
            if token is None:
                result, token = reviews(
                    app_id,
                    lang='en',
                    country='us',
                    sort=Sort.NEWEST,
                    count=batch_size
                )
            else:
                result, token = reviews(
                    app_id,
                    lang='en',
                    country='us',
                    sort=Sort.NEWEST,
                    count=batch_size,
                    continuation_token=token
                )
            
            attempts += 1
            
            if not result or len(result) == 0:
                print(f"⚠ No reviews returned in batch {attempts} — stopping.")
                break

            print(f"  ✓ Fetched {len(result)} reviews (Total: {len(all_reviews) + len(result)})")

            for r in result:
                all_reviews.append({
                    "content": r.get("content", ""),
                    "score": r.get("score", None),
                    "at": r.get("at", None),
                    "bank": bank_name,
                    "source": "Google Play"
                })

            # Rate limiting
            time.sleep(2)

            if token is None:
                print(f"  ℹ No continuation token — all reviews fetched.")
                break

        except Exception as e:
            print(f"⚠ Error fetching reviews: {e}")
            print(f"  Error type: {type(e).__name__}")
            # Try to continue with next batch if we have some reviews
            if len(all_reviews) > 0:
                print(f"  Continuing with {len(all_reviews)} reviews collected so far...")
                break
            else:
                print(f"  No reviews collected yet. Skipping {bank_name}.")
                return []

    print(f"✅ Finished: {bank_name} → {len(all_reviews)} reviews")
    return all_reviews


# -------------------------
# TEST FUNCTION - Verify app IDs
# -------------------------
def verify_app_exists(app_id):
    """Verify if an app exists by fetching its basic info."""
    try:
        app_info = app(app_id, lang='en', country='us')
        return True, app_info.get('title', 'Unknown'), app_info.get('score', 0)
    except Exception as e:
        return False, None, None

def test_app_id(app_id):
    """Test if an app ID is valid by trying to fetch a small number of reviews."""
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=1
        )
        return len(result) > 0, result[0] if result else None
    except Exception as e:
        return False, str(e)

# -------------------------
# MAIN SCRIPT
# -------------------------
print("=" * 60)
print("ETHIOPIAN BANK REVIEWS SCRAPER")
print("=" * 60)

# Test app IDs first and find working ones
print("\n🧪 Testing app IDs...")
working_app_ids = {}

for bank, app_id_list in APPS.items():
    if isinstance(app_id_list, str):
        app_id_list = [app_id_list]
    
    found_working = False
    for app_id in app_id_list:
        # First verify app exists
        exists, app_name, rating = verify_app_exists(app_id)
        if exists:
            print(f"  ✓ {bank}: App found - '{app_name}' (Rating: {rating})")
            # Then test if reviews can be fetched
            has_reviews, info = test_app_id(app_id)
            if has_reviews:
                print(f"     ✓ Reviews accessible with ID: {app_id}")
                working_app_ids[bank] = app_id
                found_working = True
                break
            else:
                print(f"     ⚠ Reviews may not be available: {info}")
        else:
            print(f"  ✗ {bank}: App not found with ID '{app_id}'")
    
    if not found_working:
        print(f"  ❌ {bank}: No working app ID found. Please verify on Google Play Store.")
        working_app_ids[bank] = app_id_list[0]  # Use first as fallback

print("\n" + "=" * 60)
print("Starting full scrape...")
print("=" * 60)

all_data = []
failed_banks = []

# Use working app IDs from testing phase
for bank in APPS.keys():
    app_id = working_app_ids.get(bank, APPS[bank][0] if isinstance(APPS[bank], list) else APPS[bank])
    try:
        bank_reviews = scrape_bank_reviews(bank, app_id, total=400)
        if bank_reviews:
            all_data.extend(bank_reviews)
        else:
            failed_banks.append(bank)
    except Exception as e:
        print(f"❌ Failed to scrape {bank}: {e}")
        failed_banks.append(bank)

print("\n" + "=" * 60)
print("SCRAPING SUMMARY")
print("=" * 60)
print(f"Total reviews collected: {len(all_data)}")
print(f"Banks scraped successfully: {len(APPS) - len(failed_banks)}/{len(APPS)}")
if failed_banks:
    print(f"Failed banks: {', '.join(failed_banks)}")

if not all_data:
    print("\n❌ ERROR: No reviews scraped at all.")
    print("Possible reasons:")
    print("  1. App IDs might be incorrect")
    print("  2. Google Play Store may be blocking requests")
    print("  3. Network connectivity issues")
    print("  4. Apps might not have reviews available")
    raise Exception("❌ No reviews scraped at all. Please check app IDs and network connection.")

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Save to CSV
os.makedirs("data/raw", exist_ok=True)
output_file = "data/raw/ethiopian_bank_reviews.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"\n✅ Data saved to: {output_file}")
print(f"   Total rows: {len(df)}")
print(f"   Columns: {', '.join(df.columns.tolist())}")
print(f"\n🎉 Scraping completed!")
