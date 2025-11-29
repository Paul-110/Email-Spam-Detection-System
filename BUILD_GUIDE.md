# 🛠️ The Ultimate Build Guide: Email Spam Classifier (Backend & ML Focus)

This guide walks you through building the **core logic** of the Spam Classifier from scratch. We will focus on the "Brain" of the application: the Machine Learning model, the training pipeline, and the backend services.

---

## 📍 Phase 1: Project Setup & "Where to Build"

### 1.1 Directory Structure
Create a folder named `spam-classifier-core`. Inside, create this structure to keep logic separate from the UI.

```text
spam-classifier-core/
├── data/                   # Where raw CSV data lives
├── models/                 # Where saved .pkl files live
├── src/
│   ├── training/           # Scripts to train the AI
│   ├── preprocessing/      # Cleaning text
│   ├── models/             # Prediction logic
│   └── services/           # Business logic
└── requirements.txt        # Dependencies
```

### 1.2 Environment
Open your terminal in this folder and run:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install pandas numpy scikit-learn nltk joblib
```

---

## 🧠 Phase 2: Building the ML Model (The "Brain")

We need to teach the computer what "Spam" looks like.

### 2.1 The Dataset
You need a CSV file with two columns: `v1` (label: ham/spam) and `v2` (text).
*   **Action**: Download the "SMS Spam Collection" dataset from Kaggle or UCI.
*   **Place it**: `data/spam.csv`

### 2.2 Text Preprocessing (`src/preprocessing/text_processor.py`)
Raw text is messy. We need to clean it before the AI sees it.

```python
import re
import string

class TextProcessor:
    @staticmethod
    def clean_text(text):
        # 1. Lowercase
        text = text.lower()
        # 2. Remove special characters/punctuation
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # 3. Remove extra whitespace
        text = text.strip()
        return text
```

### 2.3 The Training Script (`src/training/train_model.py`)
This is the most critical file. It learns from data and saves the "Brain".

**Logic Breakdown:**
1.  **Load Data**: Read CSV.
2.  **Split**: Keep 20% of data hidden for testing.
3.  **Vectorize**: Convert words to numbers using **TF-IDF** (Term Frequency-Inverse Document Frequency).
4.  **Train**: Use **Multinomial Naive Bayes** (best for text counts).
5.  **Save**: Dump the trained model and vectorizer to files.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from src.preprocessing.text_processor import TextProcessor

# 1. Load Data
print("Loading data...")
df = pd.read_csv('data/spam.csv', encoding='latin-1')
df = df[['v1', 'v2']] # Keep only label and text
df.columns = ['label', 'text']

# 2. Preprocess
print("Cleaning text...")
df['clean_text'] = df['text'].apply(TextProcessor.clean_text)
# Convert labels to numbers: spam=1, ham=0
df['label_num'] = df['label'].map({'spam': 1, 'ham': 0})

# 3. Split Data
X_train, X_test, y_train, y_test = train_test_split(
    df['clean_text'], df['label_num'], test_size=0.2, random_state=42
)

# 4. Vectorization (Text -> Numbers)
print("Vectorizing...")
vectorizer = TfidfVectorizer(max_features=3000) # Keep top 3000 words
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 5. Train Model (Naive Bayes)
print("Training Naive Bayes...")
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# 6. Evaluate
predictions = model.predict(X_test_tfidf)
print(f"Accuracy: {accuracy_score(y_test, predictions)}")

# 7. Save the Brain
if not os.path.exists('models'):
    os.makedirs('models')
    
joblib.dump(model, 'models/spam_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')
print("Model saved to models/ folder!")
```

**Run it:** `python -m src.training.train_model`
**Result:** You now have `spam_model.pkl` and `vectorizer.pkl`.

---

## ⚙️ Phase 3: Backend Logic (The "Engine")

Now that we have a trained model, we need code to *load* it and *use* it.

### 3.1 Model Loader (`src/models/model_loader.py`)
We use a **Singleton Pattern** here. Why? Loading a model takes time and memory. We only want to do it ONCE, not for every single email.

```python
import joblib
import os

class ModelLoader:
    _model = None
    _vectorizer = None

    @classmethod
    def load(cls):
        # Only load if not already loaded
        if cls._model is None:
            print("Loading model files from disk...")
            cls._model = joblib.load('models/spam_model.pkl')
            cls._vectorizer = joblib.load('models/vectorizer.pkl')
        return cls._model, cls._vectorizer
```

### 3.2 The Predictor (`src/models/predictor.py`)
This class takes raw text and gives you the answer.

```python
from src.models.model_loader import ModelLoader
from src.preprocessing.text_processor import TextProcessor

class SpamPredictor:
    def __init__(self):
        self.model, self.vectorizer = ModelLoader.load()

    def predict(self, text):
        # 1. Clean
        clean_text = TextProcessor.clean_text(text)
        
        # 2. Vectorize (Transform single text to number format)
        # Note: We use .transform(), NOT .fit_transform()
        text_vector = self.vectorizer.transform([clean_text])
        
        # 3. Predict Class (0 or 1)
        prediction = self.model.predict(text_vector)[0]
        
        # 4. Predict Probability (Confidence)
        # returns [[prob_ham, prob_spam]]
        probabilities = self.model.predict_proba(text_vector)[0]
        
        return {
            "is_spam": bool(prediction == 1),
            "confidence": max(probabilities),
            "spam_probability": probabilities[1],
            "ham_probability": probabilities[0]
        }
```

---

## 🚀 Phase 4: Service Layer (Business Logic)

This is where you handle "Business Rules". For example: "If the model says 51% spam, maybe we should double-check?" or "Let's log this request".

### 4.1 Model Service (`src/services/model_service.py`)

```python
from src.models.predictor import SpamPredictor

class ModelService:
    def __init__(self):
        self.predictor = SpamPredictor()

    def analyze_email(self, email_text):
        if not email_text:
            return {"error": "Empty text"}
            
        result = self.predictor.predict(email_text)
        
        # Add Business Logic here
        # Example: If confidence is low (< 60%), mark as "Unsure"
        if result['confidence'] < 0.6:
            result['status'] = "UNCERTAIN"
        else:
            result['status'] = "CONFIDENT"
            
        return result
```

---

## 🔗 Phase 5: Putting it Together (Main Entry Point)

Finally, create a simple script to test your engine.

### 5.1 `main.py`

```python
from src.services.model_service import ModelService

def main():
    service = ModelService()
    
    # Test Case 1
    email1 = "Congratulations! You've won a $1000 Walmart gift card. Click here."
    print(f"Email: {email1}")
    print(service.analyze_email(email1))
    
    print("-" * 30)
    
    # Test Case 2
    email2 = "Hey mom, are we still meeting for lunch tomorrow?"
    print(f"Email: {email2}")
    print(service.analyze_email(email2))

if __name__ == "__main__":
    main()
```

---

## 🎓 Summary of Logic Flow

1.  **Training**: Raw CSV -> Clean -> Vectorize (TF-IDF) -> Train (Naive Bayes) -> `.pkl` files.
2.  **Loading**: Check if loaded -> If not, read `.pkl` files -> Store in memory.
3.  **Prediction**: New Email -> Clean -> Vectorize (using saved vectorizer) -> Model Predict -> Probability -> JSON Result.
