import feedparser
from datetime import datetime, timedelta
import requests

def get_tech_trends():
    print("🛠️ Scanning latest tech trends...")
    
    # 1. Hacker News (Tech)
    hn_url = "https://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i>" + str(int((datetime.now() - timedelta(hours=24)).timestamp()))
    hn_stories = requests.get(hn_url).json().get('hits', [])[:5]
    
    # 2. GitHub Trending (Repos)
    gh_url = "https://api.github.com/search/repositories?q=created:>" + (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + "&sort=stars"
    gh_repos = requests.get(gh_url, headers={"Accept": "application/vnd.github.v3+json"}).json().get('items', [])[:3]
    
    # Combine trends
    trends = [story['title'] for story in hn_stories] + \
             [repo['name'] + " " + repo['description'] for repo in gh_repos]
    
    print("✅ Found trends:", trends)
    return trends

if __name__ == "__main__":
    get_tech_trends()
