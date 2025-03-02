from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, YOUTUBE_MAX_RESULTS

class EvaluationAgent:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    def categorize_query(self, query):
        """Categorize the query based on keywords"""
        query_lower = query.lower()
        if any(word in query_lower for word in ["how", "tutorial", "learn"]):
            return "Educational"
        elif any(word in query_lower for word in ["news", "update", "latest"]):
            return "News"
        return "Entertainment"

    def fetch_videos(self, query):
        """Fetch relevant YouTube videos based on the query"""
        search_response = self.youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=YOUTUBE_MAX_RESULTS
        ).execute()

        video_links = []
        for item in search_response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_links.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")
        return video_links

    def evaluate(self, state):
        """Process a query and return category and relevant video links"""
        query = state["query"]
        category = self.categorize_query(query)
        video_links = self.fetch_videos(query)
        return {"category": category, "video_links": video_links}
