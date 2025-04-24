import os
import gradio as gr
from models.pii_masker import PIIMasker
from models.classifier import EmailClassifier
# Initialize models
masker = PIIMasker()
classifier = EmailClassifier()

# Load pre-trained model if it exists
MODEL_PATH = "models/email_classifier.joblib"
if os.path.exists(MODEL_PATH):
    classifier.load_model(MODEL_PATH)
else:
    print("Warning: Pre-trained model not found. "
          "Classification will not work properly.")


def classify_email(email_text):
    """
    Classify the given email text.

    Args:
        email_text (str): The email text to classify

    Returns:
        str: The classification result
    """
    if not email_text.strip():
        return "Please enter an email text to classify."

    result = classifier.predict([email_text])
    return f"Classification: {result[0]}"


def mask_pii(email_text):
    """
    Mask personally identifiable information in the email text.

    Args:
        email_text (str): The email text to mask PII from

    Returns:
        tuple: (masked_email, entities_found)
    """
    if not email_text.strip():
        return "Please enter an email text to mask PII.", "No entities found."

    masked_email, entities = masker.mask_pii(email_text)

    entities_text = ""
    for entity in entities:
        entities_text += f"- {entity['classification']}: {entity['entity']}\n"

    if not entities:
        entities_text = "No PII entities detected."

    return masked_email, entities_text


def process_email(email_text, mask_pii_option=True):
    """
    Process the email by optionally masking PII and classifying it.

    Args:
        email_text (str): The email text to process
        mask_pii_option (bool): Whether to mask PII before classification

    Returns:
        tuple: (processed_email, entities_found, classification)
    """
    if not email_text.strip():
        return ("Please enter an email text.", "No processing performed.",
                "No classification performed.")

    entities_text = "PII masking was not selected."
    processed_email = email_text

    if mask_pii_option:
        processed_email, entities_text = mask_pii(email_text)

    classification = classify_email(processed_email)

    return processed_email, entities_text, classification


# Create Gradio interface
with gr.Blocks(title="Email Classification System") as demo:
    gr.Markdown("# Email Classification System")
    gr.Markdown("This application classifies emails and can mask personally "
                "identifiable information (PII).")

    with gr.Tab("Process Email"):
        with gr.Row():
            with gr.Column():
                input_email = gr.Textbox(
                    label="Input Email Text",
                    placeholder="Enter email text here...",
                    lines=10
                )
                mask_checkbox = gr.Checkbox(
                    label="Mask PII before classification",
                    value=True
                )
                process_button = gr.Button("Process Email")

            with gr.Column():
                output_email = gr.Textbox(
                    label="Processed Email",
                    lines=10,
                    interactive=False
                )
                entities_found = gr.Textbox(
                    label="PII Entities Detected",
                    lines=5,
                    interactive=False
                )
                classification_result = gr.Textbox(
                    label="Classification Result",
                    interactive=False
                )

    with gr.Tab("About"):
        gr.Markdown("""
        ## About This Application

        This application provides two main functionalities:

1. **PII Masking**: Detects and masks personally identifiable information in
emails
2. **Email Classification**: Classifies emails into predefined categories

        The system can be used to preprocess emails for data privacy compliance
        and to organize emails by type.
        """)

    process_button.click(
        fn=process_email,
        inputs=[input_email, mask_checkbox],
        outputs=[output_email, entities_found, classification_result]
    )


# Launch the app
if __name__ == "__main__":
    demo.launch()
