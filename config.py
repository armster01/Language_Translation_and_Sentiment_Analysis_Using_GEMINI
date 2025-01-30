class Config:
    # Streamlit configs
    PAGE_TITLE = "Language Translation & Sentiment Analysis"
    PAGE_ICON = "🌐"
    LAYOUT = "wide"
    
    # Gemini API settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    MODEL_NAME = "gemini-pro"
    
    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'nl': 'Dutch',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi'
    }