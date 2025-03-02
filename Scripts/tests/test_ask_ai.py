import unittest
from unittest.mock import patch, MagicMock
from agents.ask_ai import AskAIAgent  # Adjusted import if running from tests folder
from workflow import handle_query, create_workflow

class TestAskAIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AskAIAgent()

    @patch('langchain_groq.ChatGroq.invoke')
    def test_ask_ai_response(self, mock_invoke):
        """Test AI response generation"""
        # Mock Groq API response
        mock_response = MagicMock()
        mock_response.content = "Test AI response about photosynthesis"
        mock_invoke.return_value = mock_response

        # Test AI response
        result = self.agent.ask_ai({"query": "How does photosynthesis work?"})
        self.assertIn("answer", result)
        self.assertEqual(result["answer"], "Test AI response about photosynthesis")

    @patch('langchain_groq.ChatGroq.invoke', side_effect=Exception("API Error"))
    def test_ask_ai_error_handling(self, mock_invoke):
        """Test error handling in ask_ai method"""
        with self.assertRaises(Exception):
            self.agent.ask_ai({"query": "Test query"})

class TestWorkflow(unittest.TestCase):
    @patch('langchain_groq.ChatGroq.invoke')
    @patch('googleapiclient.discovery.build')
    def test_complete_workflow(self, mock_build, mock_invoke):
        """Test the complete workflow integration"""
        # Mock AI response
        mock_response = MagicMock()
        mock_response.content = "Test AI response"
        mock_invoke.return_value = mock_response

        # Mock YouTube API
        mock_youtube = MagicMock()
        mock_build.return_value = mock_youtube
        mock_youtube.search.return_value.list.return_value.execute.return_value = {
            'items': [{'id': {'kind': 'youtube#video', 'videoId': 'abc123'}}]
        }

        # Test complete workflow
        result = handle_query("How does photosynthesis work?")

        # Verify workflow output
        self.assertIn("answer", result)
        self.assertIn("category", result)
        self.assertIn("video_links", result)
        self.assertEqual(result["category"], "Educational")
        self.assertTrue(len(result["video_links"]) > 0)

if __name__ == '__main__':
    unittest.main()
