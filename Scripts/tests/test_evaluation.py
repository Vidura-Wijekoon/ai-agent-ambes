import unittest
from unittest.mock import patch, MagicMock
from agents.evaluation import EvaluationAgent

class TestEvaluationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EvaluationAgent()

    def test_categorize_query_educational(self):
        """Test educational query categorization"""
        queries = [
            "How does photosynthesis work?",
            "Tutorial on Python programming",
            "Learn to play guitar"
        ]
        for query in queries:
            self.assertEqual(self.agent.categorize_query(query), "Educational")

    def test_categorize_query_news(self):
        """Test news query categorization"""
        queries = [
            "Latest technology updates",
            "Breaking news today",
            "Update on climate change"
        ]
        for query in queries:
            self.assertEqual(self.agent.categorize_query(query), "News")

    def test_categorize_query_entertainment(self):
        """Test entertainment query categorization"""
        queries = [
            "Funny cat videos",
            "Best movies 2023",
            "Popular music videos"
        ]
        for query in queries:
            self.assertEqual(self.agent.categorize_query(query), "Entertainment")

    @patch('googleapiclient.discovery.build')
    def test_fetch_videos(self, mock_build):
        """Test YouTube video fetching"""
        # Mock YouTube API response
        mock_youtube = MagicMock()
        mock_search = MagicMock()
        mock_build.return_value = mock_youtube
        mock_youtube.search.return_value.list.return_value.execute.return_value = {
            'items': [
                {'id': {'kind': 'youtube#video', 'videoId': 'abc123'}},
                {'id': {'kind': 'youtube#video', 'videoId': 'def456'}}
            ]
        }

        # Test video fetching
        videos = self.agent.fetch_videos("test query")
        self.assertEqual(len(videos), 2)
        self.assertEqual(videos[0], "https://www.youtube.com/watch?v=abc123")
        self.assertEqual(videos[1], "https://www.youtube.com/watch?v=def456")

    def test_evaluate(self):
        """Test the complete evaluation process"""
        with patch.object(EvaluationAgent, 'fetch_videos') as mock_fetch:
            mock_fetch.return_value = [
                "https://www.youtube.com/watch?v=abc123"
            ]
            
            result = self.agent.evaluate({"query": "How to make a cake?"})
            
            self.assertEqual(result["category"], "Educational")
            self.assertEqual(len(result["video_links"]), 1)
            self.assertEqual(result["video_links"][0], "https://www.youtube.com/watch?v=abc123")

if __name__ == '__main__':
    unittest.main()
