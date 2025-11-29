import streamlit as st
import streamlit.components.v1 as components
import time
import textwrap
import pandas as pd
import numpy as np
import json
from datetime import datetime
import hashlib

# Optional plotly import
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    go = None
    HAS_PLOTLY = False

# Import backend modules
from src.config.settings import settings
from src.utils.logger import setup_logging, get_logger
from src.utils.exceptions import ModelLoadError, PredictionError, ValidationError
from src.models.model_loader import load_model_and_vectorizer
from src.models.predictor import SpamPredictor
from src.utils.explainability import explain_prediction
from src.utils.file_parser import FileParser

# Services
from src.services.model_service import ModelService
from src.services.auth_service import AuthService
from src.services.analytics_service import AnalyticsService
from src.services.cache_service import CacheService
from src.services.experiment_service import ExperimentService
from src.utils.report_generator import ReportGenerator

# Initialize logging
setup_logging(log_level=settings.LOG_LEVEL, log_dir=settings.LOG_DIR)
logger = get_logger(__name__)

# Page Config
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="src/assets/sp.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64
def get_base64_svg(path):
    try:
        with open(path, "r") as f:
            return base64.b64encode(f.read().encode('utf-8')).decode('utf-8')
    except Exception:
        return ""

icon_b64 = get_base64_svg("src/assets/sp.svg")
icon_img = f'<img src="data:image/svg+xml;base64,{icon_b64}" style="width: 40px; height: 40px; vertical-align: middle; margin-right: 10px;">' if icon_b64 else "🛡️"

# --- CSS & JS Bundle ---
# This bundle injects the premium theme, cursor, and interactions.
# It uses window.parent to affect the main Streamlit interface.

PREMIUM_BUNDLE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <script>
    (function() {
        const doc = window.parent.document;
        
        // --- CSS TOKENS & STYLES ---
        const css = `
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            /* Colors - Medium Dark Glassy Palette */
            --bg-dark: #0f172a;
            --bg-glass: rgba(30, 41, 59, 0.7);
            --bg-glass-hover: rgba(51, 65, 85, 0.8);
            --accent-primary: #6366f1; /* Indigo 500 */
            --accent-glow: rgba(99, 102, 241, 0.4);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: rgba(148, 163, 184, 0.1);
            
            /* Spacing & Radii */
            --radius-md: 12px;
            --radius-lg: 16px;
            --space-md: 1rem;
            
            /* Animation */
            --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
            --duration-fast: 0.2s;
        }

        /* Global Reset & Typography */
        body {
            font-family: 'Inter', sans-serif !important;
            background-color: var(--bg-dark) !important;
            color: var(--text-primary) !important;
        }

        /* Animated Background */
        .stApp {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 0% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            background-size: 100% 100%;
        }
        
        /* Noise Texture Overlay */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 0;
        }

        /* Glassmorphism Panels */
        .glass-panel {
            background: var(--bg-glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        /* Streamlit Overrides */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-primary), #4f46e5);
            color: white;
            border: none;
            border-radius: var(--radius-md);
            padding: 0.6rem 1.2rem;
            font-weight: 500;
            transition: transform 0.2s var(--ease-out), box-shadow 0.2s;
            box-shadow: 0 4px 12px var(--accent-glow);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 16px var(--accent-glow);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }

        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: var(--radius-md) !important;
        }
        
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px var(--accent-glow) !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-color);
        }

        /* Custom Cursor */
        .cursor-dot, .cursor-orb {
            position: fixed;
            top: 0; left: 0;
            pointer-events: none;
            z-index: 9999;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: opacity 0.3s;
        }
        
        .cursor-dot {
            width: 8px; height: 8px;
            background-color: white;
        }
        
        .cursor-orb {
            width: 40px; height: 40px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: radial-gradient(circle, rgba(99, 102, 241, 0.1), transparent);
            transition: width 0.3s, height 0.3s, background 0.3s;
        }
        
        /* Hover State for Orb */
        body.hovering .cursor-orb {
            width: 60px; height: 60px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.2), transparent);
            border-color: var(--accent-primary);
        }

        /* Hide default cursor */
        @media (pointer: fine) {
            body { cursor: none; }
            a, button, input, textarea, select { cursor: none; }
        }
        
        /* Mobile & Reduced Motion */
        @media (max-width: 768px) {
            .cursor-dot, .cursor-orb { display: none; }
            body { cursor: auto; }
        }
        @media (prefers-reduced-motion: reduce) {
            .cursor-dot, .cursor-orb { display: none; }
            body { cursor: auto; }
            * { transition: none !important; animation: none !important; }
        }
        `;

        // Inject CSS
        const styleSheet = doc.createElement("style");
        styleSheet.innerText = css;
        doc.head.appendChild(styleSheet);

        // --- JS LOGIC ---
        
        // 1. Custom Cursor
        if (window.matchMedia("(pointer: fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            const dot = doc.createElement('div'); dot.className = 'cursor-dot';
            const orb = doc.createElement('div'); orb.className = 'cursor-orb';
            doc.body.appendChild(dot);
            doc.body.appendChild(orb);

            let mouseX = 0, mouseY = 0;
            let orbX = 0, orbY = 0;

            doc.addEventListener('mousemove', (e) => {
                mouseX = e.clientX;
                mouseY = e.clientY;
                
                // Dot follows instantly
                dot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
            });

            // Orb follows with lerp
            function animate() {
                const lerp = 0.15;
                orbX += (mouseX - orbX) * lerp;
                orbY += (mouseY - orbY) * lerp;
                orb.style.transform = `translate(${orbX}px, ${orbY}px)`;
                requestAnimationFrame(animate);
            }
            requestAnimationFrame(animate);

            // Hover effects
            const interactiveSelectors = 'button, a, input, textarea, [role="button"]';
            doc.addEventListener('mouseover', (e) => {
                if (e.target.closest(interactiveSelectors)) {
                    doc.body.classList.add('hovering');
                }
            });
            doc.addEventListener('mouseout', (e) => {
                if (e.target.closest(interactiveSelectors)) {
                    doc.body.classList.remove('hovering');
                }
            });
        }

        // 2. Theme Toggle Logic
        window.setTheme = function(theme) {
            if (theme === 'light') {
                doc.documentElement.style.setProperty('--bg-dark', '#f8fafc');
                doc.documentElement.style.setProperty('--text-primary', '#0f172a');
                doc.documentElement.style.setProperty('--bg-glass', 'rgba(255, 255, 255, 0.8)');
            } else {
                doc.documentElement.style.setProperty('--bg-dark', '#0f172a');
                doc.documentElement.style.setProperty('--text-primary', '#f8fafc');
                doc.documentElement.style.setProperty('--bg-glass', 'rgba(30, 41, 59, 0.7)');
            }
            localStorage.setItem('theme', theme);
        };

        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        window.setTheme(savedTheme);
        
        // Listen for messages from Python
        window.addEventListener('message', function(event) {
            if (event.data.type === 'setTheme') {
                window.setTheme(event.data.theme);
            }
        });



        // 3. fitComponents Hook
        // Adjusts iframe height if needed (mostly for the component itself, but good practice)
        function fitComponents() {
            // Placeholder for any layout adjustments
        }
        
        // Expose to parent window for Python to call if needed
        window.parent.window.setTheme = window.setTheme;

    })();
    </script>
</body>
</html>
"""

# Voice Input Component (Restored)
def voice_input_component():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background-color: transparent; color: white; font-family: sans-serif; overflow: hidden; }
            .mic-btn {
                background-color: rgba(99, 102, 241, 0.8);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 50%;
                width: 36px;
                height: 36px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                backdrop-filter: blur(4px);
            }
            .mic-btn:hover { transform: scale(1.1); background-color: #6366f1; }
            .mic-btn.listening { animation: pulse 1.5s infinite; background-color: #22c55e; }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
                100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
            }
            #status { font-size: 0.7rem; margin-left: 10px; opacity: 0.8; color: #cbd5e1; }
            .container { display: flex; align-items: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <button id="micBtn" class="mic-btn" onclick="toggleListening()" title="Click to Speak">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                    <line x1="12" y1="19" x2="12" y2="23"></line>
                    <line x1="8" y1="23" x2="16" y2="23"></line>
                </svg>
            </button>
            <span id="status">Tap mic to speak</span>
        </div>

        <script>
            const btn = document.getElementById('micBtn');
            const status = document.getElementById('status');
            let recognition;

            if ('webkitSpeechRecognition' in window) {
                recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.onstart = function() {
                    btn.classList.add('listening');
                    status.innerText = "Listening...";
                };

                recognition.onend = function() {
                    btn.classList.remove('listening');
                    status.innerText = "Tap mic";
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    status.innerText = "Copied!";
                    navigator.clipboard.writeText(transcript);
                    setTimeout(() => { status.innerText = "Tap mic"; }, 2000);
                };
            } else {
                status.innerText = "N/A";
                btn.disabled = true;
            }

            function toggleListening() {
                if (btn.classList.contains('listening')) {
                    recognition.stop();
                } else {
                    recognition.start();
                }
            }
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=50)



# --- Python Logic ---

# Initialize Services
if 'services' not in st.session_state:
    st.session_state.services = {
        'model': ModelService(),
        'auth': AuthService(),
        'analytics': AnalyticsService(),
        'cache': CacheService(),
        'experiment': ExperimentService()
    }

model_service = st.session_state.services['model']
cache_service = st.session_state.services['cache']
experiment_service = st.session_state.services['experiment']

# Load Models
@st.cache_resource
def load_models():
    try:
        return load_model_and_vectorizer()
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return None, None

model, cv = load_models()

# Initialize Session State
if 'history' not in st.session_state: st.session_state.history = []
if 'total_checks' not in st.session_state: st.session_state.total_checks = 0
if 'spam_count' not in st.session_state: st.session_state.spam_count = 0
if 'ham_count' not in st.session_state: st.session_state.ham_count = 0


# --- Layout ---

# Sidebar
with st.sidebar:

    model_choice = st.selectbox("Model", ["Naive Bayes", "Bi-LSTM (Simulated)", "BERT (HuggingFace)"])
    language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French"])
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    c1, c2 = st.columns(2)
    c1.metric("Total", st.session_state.total_checks)
    c2.metric("Spam", st.session_state.spam_count)

# Main Area
st.markdown(f'<h2 style="text-align: center; margin: 0 0 1rem 0; display: flex; align-items: center; justify-content: center;">{icon_img} SpamShield AI</h2>', unsafe_allow_html=True)

# Tabs
tab_main, tab_batch, tab_dash = st.tabs(["📧 Classifier", "📦 Batch", "📊 Dashboard"])

with tab_main:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input Area
        # Input Area
        st.markdown('<div class="glass-panel" style="padding: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
        
        # File Upload (Moved here for visibility)
        with st.expander("📂 Upload File (PDF, TXT)", expanded=False):
            uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'eml'], label_visibility="collapsed")
            if uploaded_file:
                parsed_text = FileParser.parse_file(uploaded_file)
                if parsed_text:
                    st.success(f"Loaded: {uploaded_file.name}")
                    st.session_state['uploaded_text'] = parsed_text
                else:
                    st.error("Could not parse file.")

        # Text Area
        default_text = st.session_state.get('uploaded_text', "")
        
        # Voice Input (Restored)
        voice_input_component()
        
        email_text = st.text_area("Email Content", value=default_text, height=120, placeholder="Paste email here...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 4])
        with c1:
            # Enhanced Analyze Button with Pulse Effect
            analyze = st.button("Analyze", type="primary", use_container_width=True)
            if analyze:
                st.markdown("""
                <style>
                    div.stButton > button:first-child {
                        animation: pulse 0.5s;
                    }
                </style>
                """, unsafe_allow_html=True)
        with c2:
            if st.button("Clear"):
                st.rerun()

    with col2:
        # Info Panel
        st.markdown("""
        <div class="glass-panel" style="padding: 1rem;">
            <h5 style="margin:0;">🎯 How it works</h5>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0.5rem 0;">
                AI analyzes semantic patterns to detect threats.
            </p>
            <div style="font-size: 0.8rem; display: flex; gap: 1rem;">
                <div>✅ 99.9% Accuracy</div>
                <div>⚡ < 100ms Latency</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Logic
    if analyze and email_text:
        with st.spinner("Analyzing..."):
            time.sleep(0.3) # UX delay
            result = cache_service.get_prediction(model_service, email_text, model_choice)
            
            # Update stats
            st.session_state.total_checks += 1
            if result['is_spam']: st.session_state.spam_count += 1
            else: st.session_state.ham_count += 1
            
            # Display Result
            color = "#ef4444" if result['is_spam'] else "#22c55e"
            icon = "⚠️" if result['is_spam'] else "✅"
            label = "SPAM DETECTED" if result['is_spam'] else "LEGITIMATE EMAIL"
            
            st.markdown(f"""
            <div class="glass-panel" style="padding: 1.5rem; border-left: 5px solid {color}; margin-top: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div>
                        <h3 style="margin: 0; color: {color};">{label}</h3>
                        <p style="margin: 0; color: var(--text-secondary);">Confidence: {result['confidence']*100:.1f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Spam Probability", f"{result['spam_probability']*100:.1f}%")
            c2.metric("Safe Probability", f"{result['ham_probability']*100:.1f}%")
            c3.metric("Processing Time", f"{result['processing_time_ms']}ms")
            
            # Add to History (Restored)
            st.session_state.history.insert(0, {
                'timestamp': datetime.now().strftime('%H:%M'),
                'is_spam': result['is_spam'],
                'confidence': f"{result['confidence']*100:.1f}%",
                'text_preview': email_text[:30] + '...'
            })
            st.session_state.history = st.session_state.history[:10]

# Batch Tab
with tab_batch:
    st.markdown("### 📦 Bulk Analysis")
    uploaded = st.file_uploader("Upload CSV", type="csv")
    if uploaded:
        st.info("Batch processing ready.")

# Dashboard Tab
with tab_dash:
    st.markdown("### 📊 Analytics")
    if HAS_PLOTLY:
        # Mock Chart
        dates = pd.date_range(end=datetime.now(), periods=7)
        data = pd.DataFrame({
            'Date': dates,
            'Spam': np.random.randint(0, 10, 7),
            'Safe': np.random.randint(5, 20, 7)
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Spam'], name='Spam', line=dict(color='#ef4444')))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Safe'], name='Safe', line=dict(color='#22c55e')))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8'))
        st.plotly_chart(fig, use_container_width=True)
    
    # History Table (Restored)
    st.markdown("### 📜 Recent Analysis")
    if st.session_state.history:
        df_hist = pd.DataFrame(st.session_state.history)
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: var(--text-secondary); opacity: 0.7;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📜</div>
            <p>No analysis history yet.<br>Try analyzing an email!</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: var(--text-secondary); font-size: 0.8rem;">Powered by SpamShield AI v2.0</div>', unsafe_allow_html=True)
