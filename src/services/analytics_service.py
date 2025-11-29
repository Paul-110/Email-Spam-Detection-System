import streamlit as st
from datetime import datetime

class AnalyticsService:
    """Service for handling analytics and history."""
    
    @staticmethod
    def log_prediction(text, result):
        """Log a prediction to the session history."""
        if 'history' not in st.session_state:
            st.session_state.history = []
            
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text_preview": text[:50] + "...",
            "is_spam": result['is_spam'],
            "confidence": f"{result['confidence']:.2%}",
            "model_version": result.get('model_version', '1.0')
        }
        st.session_state.history.append(entry)
        
        # Update counters
        if 'total_checks' not in st.session_state:
            st.session_state.total_checks = 0
            st.session_state.spam_count = 0
            st.session_state.ham_count = 0
            
        st.session_state.total_checks += 1
        if result['is_spam']:
            st.session_state.spam_count += 1
        else:
            st.session_state.ham_count += 1

    @staticmethod
    def get_history():
        return st.session_state.get('history', [])
