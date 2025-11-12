"""
Named Entity Recognition (NER) service.
Extracts important entities like dates, amounts, names, etc.
"""

import re
from typing import Dict, List, Any
from datetime import datetime

class EntityExtractor:
    def __init__(self):
        # Regex patterns for common entities
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}',
            'money': r'\$?\d+(?:,\d{3})*(?:\.\d{2})?',
            'date': r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',
            'percentage': r'\d+(?:\.\d+)?%',
            'url': r'https?://(?:[-\w.])+(?:\:\d+)?(?:/[^\s]*)?',
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract various entities from text."""
        entities = {}
        
        for entity_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Remove duplicates while preserving order
                entities[entity_type] = list(dict.fromkeys(matches))
        
        # Extract invoice-specific entities
        invoice_entities = self.extract_invoice_entities(text)
        if invoice_entities:
            entities.update(invoice_entities)
        
        return entities
    
    def extract_invoice_entities(self, text: str) -> Dict[str, Any]:
        """Extract invoice-specific information."""
        entities = {}
        text_lower = text.lower()
        
        # Invoice number
        invoice_pattern = r'invoice\s*#?\s*:?\s*([A-Z0-9-]+)'
        invoice_match = re.search(invoice_pattern, text, re.IGNORECASE)
        if invoice_match:
            entities['invoice_number'] = invoice_match.group(1)
        
        # Total amount
        total_pattern = r'total\s*:?\s*\$?([0-9,]+\.?\d*)'
        total_match = re.search(total_pattern, text, re.IGNORECASE)
        if total_match:
            entities['total_amount'] = total_match.group(1)
        
        # Due date
        due_pattern = r'due\s+date\s*:?\s*([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})'
        due_match = re.search(due_pattern, text, re.IGNORECASE)
        if due_match:
            entities['due_date'] = due_match.group(1)
        
        return entities

# Singleton instance
entity_extractor = EntityExtractor()