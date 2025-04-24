# Email Classification System for Support Team

This project implements an email classification system that categorizes support emails into predefined categories while masking personal information (PII) before processing.

## Features

- **Email Classification**: Automatically categorizes support emails into different categories like Billing Issues, Technical Support, Account Management, etc.
- **PII Masking**: Detects and masks personally identifiable information including:
  - Full names
  - Email addresses
  - Phone numbers
  - Dates of birth
  - Aadhar card numbers
  - Credit/Debit card numbers
  - CVV numbers
  - Card expiry dates
- **API Deployment**: Provides a RESTful API endpoint to process and classify emails

## Project Structure

```
email-classification-system/
├── data/
│   └── emails.csv           # Sample email dataset
├── models/
│   ├── __init__.py
│   ├── classifier.py        # Email classification model
│   └── pii_masker.py        # PII masking functionality
├── utils/
│   ├── __init__.py
│   └── utils.py             # Utility functions
├── app.py                   # Main application file
├── api.py                   # API implementation
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/simon-derock/email-class.git

```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training the Model

To train the classification model with the provided dataset:

```bash
python app.py --train --data-path data/emails.csv
```

If no dataset is provided, a sample dataset will be created for testing purposes.

### Testing PII Masking

To test the PII masking functionality:

```bash
python app.py --test-masking
```

### Running the API

To start the API server:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### Classify Email

**Endpoint**: `POST /classify-email`

**Request body**:
```json
{
  "email_body": "Hello, my name is John Doe and my email is john.doe@example.com. I have an issue with my recent billing statement."
}
```

**Response**:
```json
{
    "input_email_body": "Hello, my name is John Doe and my email is john.doe@example.com. I have an issue with my recent billing statement.",
    "list_of_masked_entities": [
        {
            "position": [
                18,
                26
            ],
            "classification": "full_name",
            "entity": "John Doe"
        },
        {
            "position": [
                43,
                63
            ],
            "classification": "email",
            "entity": "john.doe@example.com"
        }
    ],
    "masked_email": "Hello, my name is [full_name] and my email is [email]. I have an issue with my recent billing statement.",
    "category_of_the_email": "Incident"
}
```

## Deployment on Hugging Face Spaces

This project is deployed on Hugging Face Spaces and can be accessed at (https://huggingface.co/spaces/philip11/email-classification-system).

## Technologies Used

- **Machine Learning**: scikit-learn, TF-IDF vectorization, Naive Bayes classification
- **PII Masking**: Regular expressions (regex) for entity recognition
- **API Development**: FastAPI, Uvicorn
- **Data Processing**: Pandas, NumPy

## Approach

1. **Data Preprocessing**: Raw emails are processed to remove noise and standardize text.
2. **PII Masking**: Regular expressions identify personal information which is then masked.
3. **Classification**: TF-IDF vectorization combined with Naive Bayes classification to categorize emails.
4. **API Integration**: FastAPI provides an easy-to-use interface for the system.

