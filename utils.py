import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def translate_text(text, source_lang, target_lang):
    """Translate text using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Create generation config to ensure consistent output
        generation_config = {
            "temperature": 0.1,  # Lower temperature for more consistent output
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        prompt = f"""
        Translate this exact text from {source_lang} to {target_lang}:
        {text}

        Important translation rules:
        1. Translate EVERYTHING, including negative statements
        2. Preserve ALL punctuation and formatting
        3. Keep the same tone and sentiment
        4. Return ONLY the translated text
        5. Do not add explanations or notes
        6. Do not modify or censor the content
        """
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if not response.text:
            raise ValueError("Empty response from API")
            
        translated_text = response.text.strip()
        # Remove any quotes that might be present
        translated_text = translated_text.strip('"\'')
        
        return translated_text
        
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None


def analyze_sentiment(text, lang):
    """Analyze sentiment of text using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        You are a sentiment analysis expert. Analyze the sentiment of the following text in {lang}.
        Text: "{text}"
        
        Return ONLY a JSON object with this exact structure, and ensure it's valid JSON:
        {{
            "sentiment": "positive/negative/neutral",
            "score": "0.0",
            "confidence": "0.0",
            "explanation": "brief explanation"
        }}
        
        Rules:
        - sentiment must be exactly one of: "positive", "negative", or "neutral"
        - score must be a number between -1 and 1
        - confidence must be a number between 0 and 1
        - explanation must be a brief string
        - Format must be exact valid JSON
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove any markdown code block indicators if present
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON response from API: {response_text}")
            return {
                "sentiment": "neutral",
                "score": "0.0",
                "confidence": "0.0",
                "explanation": "Error processing sentiment"
            }
            
    except Exception as e:
        st.error(f"Sentiment analysis error: {str(e)}")
        return None

def generate_word_cloud(text):
    """Generate word cloud from text"""
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=100
        ).generate(text)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        return plt
    except Exception as e:
        st.error(f"Word cloud generation error: {str(e)}")
        return None

def get_sentiment_color(score):
    """Get color based on sentiment score"""
    if score > 0.3:
        return "green"
    elif score < -0.3:
        return "red"
    return "gray"