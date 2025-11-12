import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Document {
  document_id: string;
  filename: string;
  success: boolean;
  page_count: number;
  confidence: number;
  text_length: number;
  document_type: string;
  classification: string;
  word_count: number;
  char_count: number;
  advanced_analysis?: any;
  uploaded_at?: string;
  content?: string;
}

export interface ProcessResponse {
  document_id: string;
  filename: string;
  success: boolean;
  page_count: number;
  confidence: number;
  text_length: number;
  document_type: string;
  classification: string;
  word_count: number;
  char_count: number;
}

export interface BatchResponse {
  total: number;
  successful: number;
  failed: number;
  results: ProcessResponse[];
}

export const uploadDocument = async (file: File, useAdvanced: boolean = false): Promise<ProcessResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/v1/upload', formData, {
    params: { use_advanced: useAdvanced },
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const batchUpload = async (files: File[], useAdvanced: boolean = false): Promise<BatchResponse> => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });
  
  const response = await api.post('/api/ocr/batch', formData, {
    params: { use_advanced: useAdvanced },
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getDocument = async (documentId: string, includeText: boolean = false): Promise<Document> => {
  const response = await api.get(`/api/ocr/document/${documentId}`, {
    params: { include_text: includeText },
  });
  return response.data;
};

export const extractText = async (file: File): Promise<any> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/ocr/extract-text', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/api/ocr/health');
  return response.data;
};

export default api;

// Add this function to process documents
export const processDocument = async (documentId: string | number): Promise<any> => {
  const response = await api.post(`/api/v1/process/${documentId}`);
  return response.data;
};

// Function to get all documents
export const getDocuments = async (): Promise<any> => {
  const response = await api.get('/api/v1/documents');
  return response.data;
};

// Function to get a single document with extracted text
export const getDocumentDetails = async (documentId: string | number): Promise<any> => {
  const response = await api.get(`/api/v1/documents/${documentId}`);
  return response.data;
};
