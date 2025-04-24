import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib
import os

class EmailClassifier:
    """
    Class to classify emails into different support categories
    using a machine learning model.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the classifier.
        
        Args:
            model_path: Path to saved model file (optional)
        """
        if model_path and os.path.exists(model_path):
            self.pipeline = joblib.load(model_path)
        else:
            # Define a simple pipeline with TF-IDF and MultinomialNB
            self.pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ('classifier', MultinomialNB())
            ])
    
    def train(self, X, y):
        """
        Train the classifier with labeled data.
        
        Args:
            X: List of email texts
            y: List of corresponding categories
        """
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.pipeline.predict(X_test)
        report = classification_report(y_test, y_pred)
        print(f"Model Evaluation:\n{report}")
        
        return report
    
    def classify(self, email_text):
        """
        Classify an email into a support category.
        
        Args:
            email_text: Text of the email to classify
            
        Returns:
            str: Predicted category
        """
        if not hasattr(self, 'pipeline') or self.pipeline is None:
            raise ValueError("Model not trained or loaded")
        
        # Make prediction
        category = self.pipeline.predict([email_text])[0]
        return category
    
    def save_model(self, model_path):
        """
        Save the trained model to disk.
        
        Args:
            model_path: Path where model should be saved
        """
        if not hasattr(self, 'pipeline') or self.pipeline is None:
            raise ValueError("No model to save")
        
        joblib.dump(self.pipeline, model_path)
        print(f"Model saved to {model_path}")
    
    @staticmethod
    def load_data(data_path):
        """
        Load email data from CSV file.
        
        Args:
            data_path: Path to CSV file with email data
            
        Returns:
            tuple: (X, y) where X is list of emails and y is list of categories
        """
        # Load data
        df = pd.read_csv(data_path)
        
        # Extract features and target
        X = df['email'].tolist()
        y = df['type'].tolist()
        
        return X, y