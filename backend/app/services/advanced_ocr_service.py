"""
Advanced OCR Service using ML models for document understanding.
"""
import torch
from transformers import (
    LayoutLMv3Processor,
    LayoutLMv3ForTokenClassification,
    DonutProcessor,
    VisionEncoderDecoderModel
)
from typing import List, Dict, Any, Optional
import logging
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

class AdvancedOCRService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        self._models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load advanced ML models for document understanding"""
        try:
            # LayoutLMv3 for document understanding
            logger.info("Loading LayoutLMv3 model...")
            self.layoutlm_processor = LayoutLMv3Processor.from_pretrained(
                "microsoft/layoutlmv3-base"
            )
            self.layoutlm_model = LayoutLMv3ForTokenClassification.from_pretrained(
                "microsoft/layoutlmv3-base"
            ).to(self.device)
            
            # Donut for document parsing (optional - comment out if too large)
            logger.info("Loading Donut model...")
            self.donut_processor = DonutProcessor.from_pretrained(
                "naver-clova-ix/donut-base"
            )
            self.donut_model = VisionEncoderDecoderModel.from_pretrained(
                "naver-clova-ix/donut-base"
            ).to(self.device)
            
            self._models_loaded = True
            logger.info("Advanced OCR models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            logger.warning("Falling back to basic OCR. Install transformers and download models for advanced features.")
            self.layoutlm_processor = None
            self.layoutlm_model = None
            self.donut_processor = None
            self.donut_model = None
            self._models_loaded = False
    
    def extract_layout_features(self, image: Image.Image, ocr_result: Dict) -> Dict:
        """Extract layout understanding from document"""
        if not self.layoutlm_model or not self._models_loaded:
            return {
                "error": "Advanced models not loaded",
                "layout_labels": [],
                "document_structure": {}
            }
        
        try:
            # Extract words and bounding boxes from OCR result
            words = ocr_result.get("words", [])
            boxes = ocr_result.get("boxes", [])
            
            if not words:
                return {
                    "layout_labels": [],
                    "document_structure": {}
                }
            
            # Prepare text and boxes
            text_list = [w.get("text", "") for w in words]
            box_list = [w.get("bbox", [0, 0, 0, 0]) for w in words]
            
            # Prepare inputs for LayoutLM
            encoding = self.layoutlm_processor(
                image,
                text_list,
                boxes=box_list,
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=512
            )
            
            # Move to device
            encoding = {k: v.to(self.device) for k, v in encoding.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.layoutlm_model(**encoding)
                predictions = outputs.logits.argmax(-1).squeeze().tolist()
            
            # Handle single prediction case
            if isinstance(predictions, int):
                predictions = [predictions]
            
            # Map predictions to labels
            labels = self._map_layout_labels(predictions, text_list)
            
            return {
                "layout_labels": labels,
                "document_structure": self._analyze_structure(labels)
            }
        except Exception as e:
            logger.error(f"Error in layout extraction: {e}")
            return {
                "error": str(e),
                "layout_labels": [],
                "document_structure": {}
            }
    
    def _map_layout_labels(self, predictions: List[int], words: List[str]) -> List[Dict]:
        """Map predicted labels to words"""
        label_map = {
            0: "OTHER",
            1: "HEADER",
            2: "QUESTION",
            3: "ANSWER",
            4: "TITLE",
            5: "TABLE",
            6: "LIST",
            7: "FOOTER",
            8: "CAPTION",
            9: "PARAGRAPH"
        }
        
        labeled_words = []
        for i, (pred, word) in enumerate(zip(predictions[:len(words)], words)):
            labeled_words.append({
                "word": word,
                "label": label_map.get(pred, "OTHER"),
                "position": i,
                "confidence": 0.0  # Could add confidence scores if available
            })
        
        return labeled_words
    
    def _analyze_structure(self, labels: List[Dict]) -> Dict:
        """Analyze document structure from labels"""
        structure = {
            "has_headers": any(l["label"] == "HEADER" for l in labels),
            "has_tables": any(l["label"] == "TABLE" for l in labels),
            "has_lists": any(l["label"] == "LIST" for l in labels),
            "has_questions": any(l["label"] == "QUESTION" for l in labels),
            "sections": self._identify_sections(labels),
            "statistics": self._calculate_statistics(labels)
        }
        return structure
    
    def _identify_sections(self, labels: List[Dict]) -> List[Dict]:
        """Identify document sections"""
        sections = []
        current_section = None
        
        for label in labels:
            if label["label"] in ["TITLE", "HEADER"]:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "title": label["word"],
                    "type": label["label"],
                    "content": [],
                    "start_position": label["position"]
                }
            elif current_section:
                current_section["content"].append(label["word"])
        
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def _calculate_statistics(self, labels: List[Dict]) -> Dict:
        """Calculate label statistics"""
        from collections import Counter
        
        label_counts = Counter(l["label"] for l in labels)
        total = len(labels)
        
        return {
            "total_elements": total,
            "label_distribution": dict(label_counts),
            "percentages": {
                label: (count / total * 100) if total > 0 else 0
                for label, count in label_counts.items()
            }
        }
    
    def extract_tables(self, image: Image.Image, ocr_result: Dict) -> List[Dict]:
        """Extract tables from document"""
        tables = []
        
        # Simple table detection based on layout
        layout_features = self.extract_layout_features(image, ocr_result)
        
        if layout_features.get("document_structure", {}).get("has_tables"):
            # Group TABLE labeled elements
            table_elements = [
                l for l in layout_features.get("layout_labels", [])
                if l["label"] == "TABLE"
            ]
            
            if table_elements:
                tables.append({
                    "type": "detected_table",
                    "elements": table_elements,
                    "confidence": 0.8
                })
        
        return tables
    
    def extract_forms(self, image: Image.Image, ocr_result: Dict) -> Dict:
        """Extract form fields from document"""
        layout_features = self.extract_layout_features(image, ocr_result)
        
        # Find question-answer pairs
        questions = []
        answers = []
        
        for label in layout_features.get("layout_labels", []):
            if label["label"] == "QUESTION":
                questions.append(label)
            elif label["label"] == "ANSWER":
                answers.append(label)
        
        # Pair questions with answers
        form_fields = []
        for q in questions:
            # Find nearest answer
            nearest_answer = None
            min_distance = float('inf')
            
            for a in answers:
                distance = abs(a["position"] - q["position"])
                if distance < min_distance and a["position"] > q["position"]:
                    min_distance = distance
                    nearest_answer = a
            
            if nearest_answer:
                form_fields.append({
                    "question": q["word"],
                    "answer": nearest_answer["word"],
                    "confidence": 0.7
                })
        
        return {
            "form_fields": form_fields,
            "total_fields": len(form_fields),
            "has_forms": len(form_fields) > 0
        }
    
    def process_with_donut(self, image: Image.Image) -> Dict:
        """Process document with Donut model for parsing"""
        if not self.donut_model or not self._models_loaded:
            return {"error": "Donut model not loaded"}
        
        try:
            # Prepare image
            pixel_values = self.donut_processor(image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            
            # Generate output
            with torch.no_grad():
                outputs = self.donut_model.generate(
                    pixel_values,
                    max_length=512,
                    early_stopping=True,
                    pad_token_id=self.donut_processor.tokenizer.pad_token_id,
                    eos_token_id=self.donut_processor.tokenizer.eos_token_id,
                    decoder_start_token_id=self.donut_processor.tokenizer.convert_tokens_to_ids(['<s>'])[0]
                )
            
            # Decode output
            decoded = self.donut_processor.batch_decode(outputs, skip_special_tokens=True)[0]
            
            return {
                "parsed_content": decoded,
                "model": "donut"
            }
        except Exception as e:
            logger.error(f"Error in Donut processing: {e}")
            return {"error": str(e)}
    
    def analyze_document(self, image_path: str, ocr_result: Dict) -> Dict:
        """Complete document analysis with all advanced features"""
        try:
            # Load image
            image = Image.open(image_path).convert("RGB")
            
            # Extract all features
            layout_features = self.extract_layout_features(image, ocr_result)
            tables = self.extract_tables(image, ocr_result)
            forms = self.extract_forms(image, ocr_result)
            
            # Optional: Donut parsing (comment out if too slow)
            # donut_result = self.process_with_donut(image)
            
            return {
                "layout": layout_features,
                "tables": tables,
                "forms": forms,
                # "donut_parsing": donut_result,
                "summary": {
                    "has_structure": bool(layout_features.get("document_structure", {}).get("sections")),
                    "table_count": len(tables),
                    "form_field_count": forms.get("total_fields", 0),
                    "document_type": self._infer_document_type(layout_features, tables, forms)
                }
            }
        except Exception as e:
            logger.error(f"Error in document analysis: {e}")
            return {"error": str(e)}
    
    def _infer_document_type(self, layout: Dict, tables: List, forms: Dict) -> str:
        """Infer document type from analysis"""
        structure = layout.get("document_structure", {})
        
        if forms.get("total_fields", 0) > 5:
            return "form"
        elif len(tables) > 0:
            return "report_with_tables"
        elif structure.get("has_questions"):
            return "questionnaire"
        elif structure.get("has_lists"):
            return "list_document"
        elif structure.get("sections", []):
            return "structured_document"
        else:
            return "unstructured_document"

# Create singleton instance
advanced_ocr_service = AdvancedOCRService()