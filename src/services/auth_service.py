import streamlit as st

class AuthService:
    """Service for handling user authentication (Simulated)."""
    
    @staticmethod
    def check_auth():
        """Simple check to ensure user is 'logged in'."""
        if 'user' not in st.session_state:
            st.session_state.user = {'username': 'Guest', 'role': 'User'}
        return st.session_state.user

    @staticmethod
    def login(username, password):
        """Simulate login."""
        if username and password:
            st.session_state.user = {'username': username, 'role': 'Admin'}
            return True
        return False
