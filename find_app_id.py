"""
Helper script to find the correct Google Play Store app ID for a bank app.

Usage:
    python find_app_id.py "CBE Mobile Banking"
    
Or search for the app manually on Google Play Store and look at the URL:
    https://play.google.com/store/apps/details?id=APP_ID_HERE
"""

from google_play_scraper import search

def search_app(query):
    """Search for an app on Google Play Store."""
    try:
        print(f"\n[SEARCH] Searching for: '{query}'...\n")
    except UnicodeEncodeError:
        print(f"\nSearching for: '{query}'...\n")
    
    try:
        results = search(query, lang='en', country='us', n_hits=5)
        
        if not results:
            print("[ERROR] No apps found. Try a different search query.")
            return
        
        print(f"Found {len(results)} results:\n")
        for i, result in enumerate(results, 1):
            app_id = result.get('appId')
            title = result.get('title', 'Unknown')
            developer = result.get('developer', 'Unknown')
            rating = result.get('score', 0)
            
            print(f"{i}. {title}")
            if app_id:
                print(f"   App ID: {app_id}")
            else:
                print(f"   App ID: Not available (try searching on Google Play Store)")
            print(f"   Developer: {developer}")
            print(f"   Rating: {rating if rating else 'N/A'}")
            
            # Try to get more info if app_id is available
            if app_id:
                try:
                    from google_play_scraper import app as get_app
                    app_info = get_app(app_id, lang='en', country='us')
                    print(f"   Package: {app_info.get('appId', 'N/A')}")
                    print(f"   Installs: {app_info.get('installs', 'N/A')}")
                except:
                    pass
            print()
            
    except Exception as e:
        print(f"[ERROR] Error searching: {e}")
        print("\n💡 Tip: You can also find the app ID manually:")
        print("   1. Go to Google Play Store")
        print("   2. Search for the app")
        print("   3. Open the app page")
        print("   4. Look at the URL: play.google.com/store/apps/details?id=APP_ID_HERE")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search_app(query)
    else:
        print("Usage: python find_app_id.py 'App Name'")
        print("\nExample searches:")
        print("  python find_app_id.py 'CBE Mobile Banking'")
        print("  python find_app_id.py 'Bank of Abyssinia'")
        print("  python find_app_id.py 'Dashen Bank'")

