import streamlit as st
from config import Config
import plotly.graph_objects as go

def render_header():
    """Render the application header"""
    st.title("🌐 Language Translation & Sentiment Analysis")
    st.markdown("""
    Translate text between multiple languages and analyze its sentiment using AI.
    Upload text or type directly to get started!
    """)

def render_language_selector(label, default_lang="en"):
    """Render a language selection dropdown"""
    return st.selectbox(
        label,
        options=Config.LANGUAGES.keys(),
        format_func=lambda x: Config.LANGUAGES[x],
        index=list(Config.LANGUAGES.keys()).index(default_lang)
    )

def render_text_input():
    """Render text input area"""
    input_method = st.radio(
        "Choose input method:",
        ["Type text", "Upload file"]
    )
    
    if input_method == "Type text":
        return st.text_area("Enter your text:", height=150)
    else:
        uploaded_file = st.file_uploader("Upload a text file", type=['txt'])
        if uploaded_file is not None:
            return uploaded_file.getvalue().decode()
        return None

def render_sentiment_gauge(sentiment_data):
    """Render sentiment gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(sentiment_data['score']) * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [-100, 100]},
            'bar': {'color': get_sentiment_color(float(sentiment_data['score']))},
            'steps': [
                {'range': [-100, -30], 'color': "lightpink"},
                {'range': [-30, 30], 'color': "lightgray"},
                {'range': [30, 100], 'color': "lightgreen"}
            ]
        },
        title = {'text': "Sentiment Score"}
    ))
    
    st.plotly_chart(fig)

def get_sentiment_color(score):
    """Get color based on sentiment score"""
    if score > 0.3:
        return "green"
    elif score < -0.3:
        return "red"
    return "gray"