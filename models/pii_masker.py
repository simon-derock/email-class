import re
from typing import Dict, List, Tuple

class PIIMasker:
    """
    Class to mask personally identifiable information (PII) in text.
    Uses regular expressions to identify and mask PII.
    """
    
    def __init__(self):
        # Define regex patterns for each PII type
        self.patterns = {
            "full_name": r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone_number": r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b',
            "dob": r'\b(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[012])[-/.](19|20)\d\d\b',
            "aadhar_num": r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b',
            "credit_debit_no": r'\b(?:\d[ -]*?){13,16}\b',
            "cvv_no": r'\bCVV:? \d{3,4}\b|\bCVV \d{3,4}\b',
            "expiry_no": r'\b(0[1-9]|1[0-2])/\d{2,4}\b'
        }
    
    def mask_pii(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Mask PII in the input text.
        
        Args:
            text: Input text containing PII
            
        Returns:
            tuple: (masked_text, list_of_entities)
        """
        masked_text = text
        entities = []
        
        # Process each PII type
        for entity_type, pattern in self.patterns.items():
            # Find all matches
            for match in re.finditer(pattern, text):
                start_idx, end_idx = match.span()
                original_entity = match.group()
                
                # Store entity information
                entity_info = {
                    "position": [start_idx, end_idx],
                    "classification": entity_type,
                    "entity": original_entity
                }
                entities.append(entity_info)
        
        # Sort entities by start position in reverse to avoid index shifting
        entities.sort(key=lambda x: x["position"][0], reverse=True)
        
        # Replace entities with masks
        for entity in entities:
            start_idx, end_idx = entity["position"]
            entity_type = entity["classification"]
            masked_text = masked_text[:start_idx] + f"[{entity_type}]" + masked_text[end_idx:]
        
        # Re-sort entities by start position for output
        entities.sort(key=lambda x: x["position"][0])
        
        return masked_text, entities