import streamlit as st
import sys
import os

# Insert the current script directory to the beginning of sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

# Now import handle_query from Scripts package
from Scripts import handle_query

# Set page config
st.set_page_config(
    page_title="EduHelper",
    page_icon="🤖",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .stVideo {
        margin-bottom: 1rem;
    }
    .video-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 EduHelper")

# User input
query = st.text_input("Ask your question:", placeholder="Type your question here...")

# Process query when submitted
if query:
    with st.spinner("Processing your query..."):
        try:
            # Get response from AI agent
            result = handle_query(query)
            
            # Display AI answer
            st.header("🤔 AI Answer")
            st.write(result["answer"])
            
            # Display category
            st.header("📑 Category")
            category_color = {
                "Educational": "blue",
                "News": "orange",
                "Entertainment": "green"
            }.get(result["category"], "gray")
            st.markdown(f"<h3 style='color: {category_color};'>{result['category']}</h3>", unsafe_allow_html=True)
            
            # Display videos
            st.header("🎥 Related Videos")
            if result["video_links"]:
                st.markdown("<div class='video-container'>", unsafe_allow_html=True)
                for video_link in result["video_links"]:
                    st.video(video_link)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No related videos found.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add instructions in the sidebar
with st.sidebar:
    st.header("📝 Instructions")
    st.markdown("""
    1. Type your question in the input box  
    2. Press Enter to submit  
    3. View the AI's answer  
    4. Check the query category  
    5. Watch related YouTube videos  
    """)
    
    st.header("ℹ️ About")
    st.markdown("""
    This AI assistant helps you find answers to your questions and suggests relevant
    YouTube videos. The system categorizes your query and provides both an AI-generated
    answer and curated video content.
    """)
