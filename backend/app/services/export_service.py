"""Export Service - Generate Excel and CSV files with extracted text"""
import pandas as pd
import io
from typing import List, Dict

class ExportService:
    def export_to_excel(self, documents: List[Dict]) -> bytes:
        df = pd.DataFrame(documents)
        columns_map = {
            'id': 'ID', 'filename': 'Filename', 'file_type': 'Type',
            'status': 'Status', 'confidence': 'Confidence (%)',
            'document_type': 'Document Type', 'created_at': 'Upload Date',
            'word_count': 'Word Count', 'extracted_text': 'Extracted Text'
        }
        available_cols = [col for col in columns_map.keys() if col in df.columns]
        df_export = df[available_cols].copy()
        df_export.columns = [columns_map[col] for col in available_cols]
        
        # Truncate long text for Excel
        if 'Extracted Text' in df_export.columns:
            df_export['Extracted Text'] = df_export['Extracted Text'].apply(
                lambda x: str(x)[:32000] if pd.notna(x) else ''
            )
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Documents')
            worksheet = writer.sheets['Documents']
            for idx, col in enumerate(df_export.columns):
                max_length = min(max(df_export[col].astype(str).str.len().max(), len(col)) + 2, 50)
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        output.seek(0)
        return output.getvalue()
    
    def export_to_csv(self, documents: List[Dict]) -> str:
        df = pd.DataFrame(documents)
        columns_map = {
            'id': 'ID', 'filename': 'Filename', 'file_type': 'Type',
            'status': 'Status', 'confidence': 'Confidence',
            'document_type': 'Document Type', 'created_at': 'Upload Date',
            'word_count': 'Word Count', 'extracted_text': 'Extracted Text'
        }
        available_cols = [col for col in columns_map.keys() if col in df.columns]
        df_export = df[available_cols].copy()
        df_export.columns = [columns_map[col] for col in available_cols]
        return df_export.to_csv(index=False)

_export_service = None

def get_export_service():
    global _export_service
    if _export_service is None:
        _export_service = ExportService()
    return _export_service
