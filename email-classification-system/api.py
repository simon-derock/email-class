from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from models.pii_masker import PIIMasker
from models.classifier import EmailClassifier
from utils.utils import preprocess_email

# Initialize FastAPI app
app = FastAPI(title="Email Classification API",
              description="API for classifying support emails and masking PII",
              version="1.0.0")

# Initialize PII masker and classifier
pii_masker = PIIMasker()
classifier = EmailClassifier(model_path="models/email_classifier.joblib")


class EmailRequest(BaseModel):
    email_body: str


class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: list
    masked_email: str
    category_of_the_email: str


@app.post("/classify-email", response_model=EmailResponse)
async def classify_email(request: EmailRequest = Body(...)):
    """
    Classify an email and mask PII information.

    Args:
        request: Email request object containing the email body

    Returns:
        dict: Response with masked email and classification
    """
    try:
        email_body = request.email_body

        # Mask PII
        masked_email, entities = pii_masker.mask_pii(email_body)

        # Preprocess for classification
        processed_email = preprocess_email(masked_email)

        # Classify email
        category = classifier.classify(processed_email)

        # Prepare response
        response = {
            "input_email_body": email_body,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category
        }

        return response

    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status message
    """
    return {"status": "healthy"}


# For local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
