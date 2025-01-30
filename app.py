import streamlit as st
from config import Config
from utils import translate_text, analyze_sentiment, generate_word_cloud
from components import (
    render_header,
    render_language_selector,
    render_text_input,
    render_sentiment_gauge
)

# Configure page settings
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout=Config.LAYOUT
)

def main():
    render_header()
    
    # Input section
    st.header("📝 Input Text")
    text = render_text_input()
    
    if text:
        # Language selection
        col1, col2 = st.columns(2)
        with col1:
            source_lang = render_language_selector("Source Language")
        with col2:
            target_lang = render_language_selector("Target Language", "es")
        
        # Translation
        if st.button("Translate"):
            with st.spinner("Translating..."):
                translated_text = translate_text(text, 
                                              Config.LANGUAGES[source_lang],
                                              Config.LANGUAGES[target_lang])
                if translated_text:
                    st.header("🔄 Translation")
                    st.text_area("Translated Text:", translated_text, height=150)
                    
                    # Sentiment Analysis
                    st.header("😊 Sentiment Analysis")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Original Text")
                        with st.spinner("Analyzing original text..."):
                            original_sentiment = analyze_sentiment(
                                text, 
                                Config.LANGUAGES[source_lang]
                            )
                            if original_sentiment:
                                render_sentiment_gauge(original_sentiment)
                                st.markdown(f"**Explanation:** {original_sentiment['explanation']}")
                    
                    with col2:
                        st.subheader("Translated Text")
                        with st.spinner("Analyzing translated text..."):
                            translated_sentiment = analyze_sentiment(
                                translated_text,
                                Config.LANGUAGES[target_lang]
                            )
                            if translated_sentiment:
                                render_sentiment_gauge(translated_sentiment)
                                st.markdown(f"**Explanation:** {translated_sentiment['explanation']}")
                    
                    # Word Cloud
                    st.header("☁️ Word Cloud")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Original Text")
                        fig = generate_word_cloud(text)
                        if fig:
                            st.pyplot(fig)
                    
                    with col2:
                        st.subheader("Translated Text")
                        fig = generate_word_cloud(translated_text)
                        if fig:
                            st.pyplot(fig)

if __name__ == "__main__":
    main()