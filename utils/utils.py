import os
import pandas as pd
import re

def preprocess_email(email_text):
    """
    Preprocess email text for better classification.
    
    Args:
        email_text: Raw email text
        
    Returns:
        str: Preprocessed email text
    """
    # Convert to lowercase
    email_text = email_text.lower()
    
    # Remove email headers (if present)
    email_text = re.sub(r'from:.*?\n', '', email_text)
    email_text = re.sub(r'to:.*?\n', '', email_text)
    email_text = re.sub(r'subject:.*?\n', '', email_text)
    email_text = re.sub(r'date:.*?\n', '', email_text)
    
    # Remove special characters and extra whitespace
    email_text = re.sub(r'[^\w\s]', ' ', email_text)
    email_text = re.sub(r'\s+', ' ', email_text).strip()
    
    return email_text

def parse_emails_dataset(file_path):
    """
    Parse the email dataset from the provided format.
    
    Args:
        file_path: Path to the email dataset file
        
    Returns:
        pd.DataFrame: DataFrame with email text and categories
    """
    if not os.path.exists(file_path):
        print(f"Warning: Dataset file {file_path} not found")
        # Create a small sample dataset for testing
        data = {
            'email': [
                "I have a problem with my billing. My card was charged twice.",
                "My account is locked and I can't log in.",
                "How do I change my password?",
                "The product I received is defective."
            ],
            'type': ['Billing', 'Account', 'Account', 'Product']
        }
        return pd.DataFrame(data)
    
    # Load data and return DataFrame
    return pd.read_csv(file_path)

def create_sample_dataset(output_path):
    """
    Create a sample dataset for testing.
    
    Args:
        output_path: Path to save the sample dataset
    """
    data = {
        'email': [
            "Hello, I'm having issues with my recent bill. I was charged twice for the same service. My name is John Smith and you can reach me at john.smith@example.com or call me at 555-123-4567.",
            "I can't access my account. It says my password is wrong but I'm sure it's correct. Please help! My customer ID is 12345 and my DOB is 15/04/1985.",
            "I need technical support for your software. It keeps crashing when I try to save my work. My email is tech.user@company.org.",
            "I want to cancel my subscription. Please process this request as soon as possible. You can contact me at 123-456-7890.",
            "The product I ordered hasn't arrived yet. Order #98765. My Aadhar number is 1234 5678 9012 and my credit card ending in 4567 expires on 12/25."
        ],
        'type': ['Billing', 'Account', 'Technical', 'Account', 'Order']
    }
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Sample dataset created at {output_path}")