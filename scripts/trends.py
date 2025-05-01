import requests
from datetime import datetime, timedelta

def get_tech_trends():
    print("🔍 Scanning Hacker News...")
    hn_url = "https://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i>" + str(int((datetime.now() - timedelta(hours=24)).timestamp()))
    hn_stories = requests.get(hn_url).json().get('hits', [])
    
    print("📊 Top 5 Tech Trends:")
    trends = [story['title'] for story in hn_stories[:5]]
    for i, trend in enumerate(trends, 1):
        print(f"{i}. {trend}")
    
    return trends

if __name__ == "__main__":
    get_tech_trends()
