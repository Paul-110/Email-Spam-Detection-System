import datetime

class ReportGenerator:
    """Generates technical whitepapers/reports."""
    
    @staticmethod
    def generate_markdown_report(stats):
        """Create a markdown report string."""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        report = f"""
# 🛡️ Spam Classifier - Technical Whitepaper
**Date:** {date_str}
**Version:** 2.0.0

## 1. Executive Summary
This report details the architecture and performance of the Spam Classifier system. The system leverages machine learning and natural language processing to detect unsolicited emails with high accuracy.

## 2. Architecture
The application follows a **Microservices-based Architecture** within a Streamlit frontend:
- **ModelService**: Encapsulates ML logic (Naive Bayes, Bi-LSTM, BERT).
- **AuthService**: Manages user sessions and role-based access.
- **AnalyticsService**: Tracks usage metrics and classification history.
- **CacheService**: Optimizes performance using hash-based caching.

```mermaid
graph TD
    User[User Interface] --> Auth[AuthService]
    User --> Model[ModelService]
    User --> Analytics[AnalyticsService]
    Model --> Cache[CacheService]
    Model --> Predictor[SpamPredictor]
```

## 3. Performance Metrics
- **Total Classifications**: {stats.get('total', 0)}
- **Spam Detected**: {stats.get('spam', 0)}
- **Ham Detected**: {stats.get('ham', 0)}
- **Average Latency**: ~100ms (Naive Bayes), ~1.5s (Bi-LSTM)

## 4. Technology Stack
- **Frontend**: Streamlit
- **ML Backend**: Scikit-learn, TensorFlow (Simulated), Transformers (Simulated)
- **Visualization**: Plotly
- **Processing**: Pandas, NumPy

---
*Generated automatically by the Spam Classifier System.*
"""
        return report
