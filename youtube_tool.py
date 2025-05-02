from phi.agent import Agent
from phi.tools.youtube_tools import YouTubeTools
from phi.model.groq import Groq
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables from .env file
load_dotenv()


def youtube_video_details(link):
    try:
        # Check if GROQ_API_KEY is set
        if not os.environ.get('GROQ_API_KEY'):
            return "Error: GROQ_API_KEY environment variable is not set. Please add it to your .env file."

        agent = Agent(
            model = Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
            tools=[YouTubeTools()],
            show_tool_calls=True,
            description="You are a YouTube agent. Obtain the captions and metadata of a YouTube video and give details.",
        )
        
        output = agent.run("Summarize this YouTube video: " + link, markdown=True)
        return output.content
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    
    html_temp = """
    <div style="background-color:cyan;padding:8px">
    <h2 style="color:black;text-align:center;">YouTube Video Summary Extraction by AI Agent</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)    
    
    # Try to load the logo if it exists, otherwise skip it
    logo_path = "logo.jpg"
    if os.path.exists(logo_path):
        st.image(logo_path, width=300)
    else:
        st.warning("Note: logo.jpg file is missing. The application will still work without it.")

    st.markdown("""
        <style>
            .stFileUploader label {
                font-size: 10px; /* Adjust font size as needed */
            }

        </style>

    """, unsafe_allow_html=True)
    
    st.markdown(
    "<p style='color: purple; font-size: 18px; font-weight: bold;'>YouTube Video Link</p>",
    unsafe_allow_html=True
    )

    link = st.text_input("")
    
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #DD3300;
        color:#eeffee;
    }
    </style>""", unsafe_allow_html=True)

    if st.button("Extract Video Summary"):
        if not link:
            st.error("Please enter a YouTube video link")
        else:
            with st.spinner("Extracting video summary..."):
                results = youtube_video_details(link)
                st.markdown(results)
    
    # Add instructions on how to set up the environment
    with st.expander("Setup Instructions"):
        st.markdown("""
        ## Setup Instructions
        
        1. Create a `.env` file in the same directory as this script
        2. Add your Groq API key to the `.env` file as follows:
           ```
           GROQ_API_KEY=your_api_key_here
           ```
        3. Optionally, add a `logo.jpg` file to the same directory for branding
        """)

if __name__=='__main__':
    main()