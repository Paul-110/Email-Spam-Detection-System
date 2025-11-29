import random
import streamlit as st

class ExperimentService:
    """Service for A/B Testing experiments."""
    
    @staticmethod
    def get_variant(experiment_name="theme_experiment"):
        """Assign a variant to the user."""
        if experiment_name not in st.session_state:
            # 50/50 split
            st.session_state[experiment_name] = 'A' if random.random() < 0.5 else 'B'
        return st.session_state[experiment_name]

    @staticmethod
    def set_variant(variant, experiment_name="theme_experiment"):
        """Manually set variant (for demo purposes)."""
        st.session_state[experiment_name] = variant

    @staticmethod
    def get_theme_css(variant):
        """Return CSS based on variant."""
        if variant == 'B':
            # Corporate Blue Theme (Variant B)
            return """
            <style>
                .stApp {
                    background-color: #0f172a;
                    background-image: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
                }
                .stButton>button {
                    background-color: #3b82f6 !important;
                    color: white !important;
                    border-radius: 4px !important;
                }
                .metric-card {
                    background: rgba(30, 58, 138, 0.4) !important;
                    border: 1px solid rgba(59, 130, 246, 0.3) !important;
                }
            </style>
            """
        else:
            # Default Dark Theme (Variant A) - already applied globally
            return ""
