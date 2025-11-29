"""
Model training script.

Trains a spam classifier using TF-IDF vectorization and Multinomial Naive Bayes.
Saves the trained model and vectorizer to disk.
"""

import sys
from pathlib import Path
# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

with open("debug.txt", "w") as f:
    f.write("Starting script\n")

print("Starting training script...")
import pandas as pd
print("Imported pandas")
import numpy as np
import pickle
import logging
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

print("Imported sklearn")
from src.preprocessing.text_processor import text_processor
from src.config.settings import settings
from src.utils.logger import setup_logging

print("Imported internal modules")

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV file handling different encodings."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded data with UTF-8 encoding. Shape: {df.shape}")
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding='latin-1')
            logger.info(f"Loaded data with Latin-1 encoding. Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns and encode targets."""
    logger.info(f"Columns found: {df.columns.tolist()}")
    
    # Check for common column names
    if 'v1' in df.columns and 'v2' in df.columns:
        df = df.rename(columns={'v1': 'target', 'v2': 'text'})
    elif 'Category' in df.columns and 'Message' in df.columns:
        df = df.rename(columns={'Category': 'target', 'Message': 'text'})
    else:
        # Fallback: Assume first column is target, second is text
        logger.warning(f"Unknown columns: {df.columns.tolist()}. Renaming first two to 'target' and 'text'")
        new_cols = ['target', 'text'] + list(df.columns[2:])
        df.columns = new_cols
    
    # Ensure required columns exist
    if 'target' not in df.columns or 'text' not in df.columns:
        raise ValueError("Data must contain 'target' and 'text' columns")
    
    # Encode target
    df['target_enc'] = df['target'].map({'spam': 1, 'ham': 0})
    
    # Drop missing values
    df.dropna(inplace=True)
    
    return df

def train_model():
    """Execute the training pipeline."""
    try:
        # Paths
        data_path = Path("spam.csv")
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # 1. Load Data
        logger.info("Loading data...")
        if not data_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        df = load_data(str(data_path))
        df = prepare_data(df)
        
        # 2. Preprocess Text
        logger.info("Preprocessing text...")
        # Use the TextProcessor for consistent cleaning
        df['processed_text'] = df['text'].apply(text_processor.clean_text)
        
        # 3. Split Data
        X = df['processed_text']
        y = df['target_enc']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Test set size: {len(X_test)}")
        
        # 4. Vectorization (TF-IDF)
        logger.info("Vectorizing data (TF-IDF)...")
        vectorizer = TfidfVectorizer(max_features=3000)
        X_train_tfidf = vectorizer.fit_transform(X_train).toarray()
        X_test_tfidf = vectorizer.transform(X_test).toarray()
        
        # 5. Train Model
        logger.info("Training Multinomial Naive Bayes model...")
        model = MultinomialNB()
        model.fit(X_train_tfidf, y_train)
        
        # 6. Evaluate
        logger.info("Evaluating model...")
        y_pred = model.predict(X_test_tfidf)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        logger.info("Model Performance:")
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1 Score:  {f1:.4f}")
        logger.info(f"Confusion Matrix:\n{cm}")
        
        # 7. Save Artifacts
        logger.info("Saving model artifacts...")
        
        # Save as v2 to distinguish from original
        model_path = models_dir / "spam_v2.pkl"
        vectorizer_path = models_dir / "vectorizer_v2.pkl"
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
            
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
            
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Vectorizer saved to {vectorizer_path}")
        
        print("\nTraining Complete! 🚀")
        print(f"Accuracy: {accuracy:.2%}")
        print(f"Saved to: {models_dir}")
        
    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    train_model()
