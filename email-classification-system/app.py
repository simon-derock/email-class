import gradio as gr
import os
from models.pii_masker import PIIMasker
from models.classifier import EmailClassifier
from utils.utils import (preprocess_email, create_sample_dataset,
                         parse_emails_dataset)

# Check if model exists, if not train it
model_path = "models/email_classifier.joblib"
if not os.path.exists(model_path):
    print("Training model as it doesn't exist yet...")
    data_path = "data/emails.csv"

    # Create sample dataset if needed
    if not os.path.exists(data_path):
        print("Creating sample dataset...")
        create_sample_dataset(data_path)

    # Train model
    df = parse_emails_dataset(data_path)
    X = df['email'].tolist()
    y = df['type'].tolist()

    classifier = EmailClassifier()
    classifier.train(X, y)

    # Save trained model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    classifier.save_model(model_path)
    print("Model trained and saved successfully!")


# Initialize components
pii_masker = PIIMasker()
classifier = EmailClassifier(model_path=model_path)


def process_email(email_body):
    """
    Process email by masking PII and classifying it.
 Args:
        email_body: Raw email text
   Returns:
        tuple: (masked_email, entities_text, category)
    """
    # Mask PII
    masked_email, entities = pii_masker.mask_pii(email_body)

    # Preprocess for classification
    processed_email = preprocess_email(masked_email)

    # Classify email
    category = classifier.classify(processed_email)

    # Format entities for display - fixed formatting
    entities_text = ""
    for entity in entities:
        entities_text += f"- {entity['classification']}: {entity['entity']}\n"

    return masked_email, entities_text, category


def test_masking():
    """Example function to demonstrate PII masking"""
    test_email = (
        "Hello, my name is John Doe, and my email is johndoe@example.com.\n"
        "My phone number is 555-123-4567 and I was born on 15/04/1985.\n"
        "My Aadhar number is 1234 5678 9012 and my credit card number is "
        "4111 1111 1111 1111 with CVV 123 expiring on 12/25."
    )
    return test_email


# Create Gradio interface
demo = gr.Interface(
    fn=process_email,
    inputs=gr.Textbox(
        lines=10,
        label="Email Content",
        placeholder="Enter email text to classify and mask PII..."
    ),
    outputs=[
        gr.Textbox(label="Masked Email"),
        gr.Textbox(label="Detected PII Entities"),
        gr.Textbox(label="Email Category")
    ],
    title="Email Classification System",
    description=(
        "This application classifies support emails and masks personally "
        "identifiable information (PII)."
    ),
    examples=[
        ["Hello, my name is John Doe, and my email is johndoe@example.com. "
         "I need help with my account."],
        ["I'm having trouble logging in to my account. My username is user"
         "123."]
    ],
    article="""
    ## How It Works
  1. **PII Masking**: The system identifies and masks personal information
    2. **Email Classification**: The masked email is classified into categories
    3. **Results**: View the masked version, detected PII, and email category
    """
)

# Launch the app
demo.launch()
