"""
Quick script to test various BOA app IDs
"""
from google_play_scraper import app, reviews, Sort

# Try different possible BOA app IDs
boa_candidates = [
    "com.ambel.mobile.android",
    "com.bankOfAbyssinia.mobilebanking", 
    "com.boa.mobile",
    "com.bankofabyssinia.mobile",
    "com.boa.mobilebanking",
    "com.abyssinia.bank.mobile"
]

print("Testing BOA App IDs...\n")

for app_id in boa_candidates:
    try:
        app_info = app(app_id, lang='en', country='us')
        title = app_info.get('title', 'Unknown')
        developer = app_info.get('developer', 'Unknown')
        rating = app_info.get('score', 0)
        
        print(f"✓ FOUND: {app_id}")
        print(f"  Title: {title}")
        print(f"  Developer: {developer}")
        print(f"  Rating: {rating}")
        
        # Test if reviews are accessible
        try:
            result, _ = reviews(app_id, lang='en', country='us', sort=Sort.NEWEST, count=1)
            if result:
                print(f"  ✓ Reviews accessible ({len(result)} sample review found)")
            else:
                print(f"  ⚠ No reviews returned")
        except Exception as e:
            print(f"  ⚠ Cannot fetch reviews: {e}")
        print()
        
    except Exception as e:
        print(f"✗ {app_id}: Not found ({type(e).__name__})")

print("\nIf none work, manually find the app ID:")
print("1. Go to https://play.google.com/store")
print("2. Search for 'Bank of Abyssinia mobile' or 'BOA mobile'")
print("3. Open the app page")
print("4. Look at the URL: play.google.com/store/apps/details?id=APP_ID_HERE")

