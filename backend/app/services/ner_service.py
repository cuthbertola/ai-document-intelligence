"""
Named Entity Recognition Service using spaCy
Extracts: Names, Organizations, Dates, Money, Locations, etc.
"""

import spacy
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class NERService:
    """Extract named entities from text"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy NER model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            self.nlp = None
    
    def extract_entities(self, text: str) -> Dict:
        """
        Extract named entities from text
        Returns: Dictionary with entity types and their values
        """
        if not self.nlp or not text:
            return {
                "persons": [],
                "organizations": [],
                "dates": [],
                "money": [],
                "locations": [],
                "emails": [],
                "phone_numbers": [],
                "all_entities": []
            }
        
        # Limit text length for performance
        text = text[:10000]
        
        doc = self.nlp(text)
        
        entities = {
            "persons": [],
            "organizations": [],
            "dates": [],
            "money": [],
            "locations": [],
            "emails": [],
            "phone_numbers": [],
            "all_entities": []
        }
        
        # Extract entities by type
        for ent in doc.ents:
            entity_info = {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            
            entities["all_entities"].append(entity_info)
            
            if ent.label_ == "PERSON":
                entities["persons"].append(ent.text)
            elif ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ in ["DATE", "TIME"]:
                entities["dates"].append(ent.text)
            elif ent.label_ == "MONEY":
                entities["money"].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities["locations"].append(ent.text)
        
        # Remove duplicates and limit results
        for key in ["persons", "organizations", "dates", "money", "locations"]:
            entities[key] = list(set(entities[key]))[:10]
        
        return entities

# Singleton
_ner_service = None

def get_ner_service():
    global _ner_service
    if _ner_service is None:
        _ner_service = NERService()
    return _ner_service
