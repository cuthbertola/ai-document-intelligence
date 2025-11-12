import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FileText, Download, Eye, Trash2, Search, RefreshCw, X, Copy, Play } from 'lucide-react';
import { processDocument } from '../services/api';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface Document {
  id: number;
  filename: string;
  file_type: string;
  status: string;
  document_type?: string;
  created_at: string;
  uploaded_at?: string;
  confidence?: number;
  page_count?: number;
  classification?: string;
}

interface DocumentDetails {
  id: number;
  filename: string;
  extracted_text?: string;
  word_count?: number;
  confidence?: number;
  processing_time?: number;
  file_size?: string;
  metadata?: any;
}

export const DocumentList: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState<DocumentDetails | null>(null);
  const [showViewer, setShowViewer] = useState(false);
  const [viewerLoading, setViewerLoading] = useState(false);
  const [entities, setEntities] = useState<any>(null);

  useEffect(() => {
    fetchDocuments();
    
    let interval: NodeJS.Timeout | undefined;
    if (autoRefresh) {
      interval = setInterval(fetchDocuments, 5000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const fetchDocuments = async () => {
    console.log("Fetching documents...");
    try {
      const response = await axios.get(`${API_URL}/api/v1/documents?limit=100`);
      console.log("Documents received:", response.data.documents);
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle View button click
  const handleView = async (doc: Document) => {
    if (doc.status !== 'completed') {
      window.alert('Document processing is not complete yet. Please wait for processing to finish.');
      return;
    }

    setViewerLoading(true);
    try {
      // Try to fetch document details from your API
      const response = await axios.get(`${API_URL}/api/v1/documents/${doc.id}`);
      setSelectedDoc(response.data);
      
      // Fetch entities
      try {
        const entitiesRes = await axios.get(`${API_URL}/api/v1/documents/${doc.id}/entities`);
        console.log("Entities loaded:", entitiesRes.data.entities);
        setEntities(entitiesRes.data.entities);
      } catch (e) {
        console.log("No entities available");
        setEntities(null);
      }
      setShowViewer(true);
    } catch (error) {
      console.error('Failed to fetch document details:', error);
      
      // If API call fails, show error message
      window.alert('Failed to load document details. The document may not have been processed yet.');
    } finally {
      setViewerLoading(false);
    }
  };

  // Handle Download button click
  const handleDownload = async (doc: Document) => {
    if (doc.status !== 'completed') {
      window.alert('Document processing is not complete yet. Cannot download extracted text.');
      return;
    }
    
    try {
      // Fetch the actual extracted text from the API
      const response = await axios.get(`${API_URL}/api/v1/documents/${doc.id}`);
      const extractedText = response.data.extracted_text;
      
      if (extractedText) {
        // Create text file with proper header
        const fileContent = `OCR Extraction Results for: ${doc.filename}
Generated: ${new Date().toLocaleString()}
Document Type: ${doc.document_type || 'Unknown'}
Status: ${doc.status}
Confidence: ${doc.confidence || 'N/A'}%
Word Count: ${response.data.word_count || 'N/A'}

========================================
EXTRACTED TEXT:
========================================

${extractedText}`;
        
        // Create and download the text file
        const blob = new Blob([fileContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${doc.filename.replace(/\.[^/.]+$/, '')}_extracted.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      } else {
        window.alert('No extracted text available for this document.');
      }
    } catch (error) {
      console.error('Download failed:', error);
      window.alert('Failed to download extracted text. Please try again.');
    }
  };

  // Handle Delete button click
  const handleDelete = async (doc: Document) => {
    if (!window.confirm(`Are you sure you want to delete "${doc.filename}"? This action cannot be undone.`)) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/v1/documents/${doc.id}`);
      window.alert(`Document "${doc.filename}" has been deleted.`);
      fetchDocuments(); // Refresh the list
    } catch (error) {
      console.error('Delete failed:', error);
      window.alert('Failed to delete document. Please try again.');
    }
  };

  // Handle Process button click for uploaded documents
  const handleProcess = async (doc: Document) => {
    const docStatus = doc.status || 'uploaded';
    if (docStatus !== 'uploaded') {
      window.alert('Document is already processed or processing.');
      return;
    }

    try {
      await processDocument(doc.id);
      window.alert(`OCR processing started for "${doc.filename}". This may take a few moments.`);
      
      // Start refreshing more frequently to show status updates
      setTimeout(() => fetchDocuments(), 2000);
      setTimeout(() => fetchDocuments(), 5000);
      setTimeout(() => fetchDocuments(), 10000);
    } catch (error) {
      console.error('Process failed:', error);
      window.alert('Failed to start OCR processing. Please try again.');
    }
  };

  // Close viewer modal
  const closeViewer = () => {
    setShowViewer(false);
    setSelectedDoc(null);
  };

  // Copy text to clipboard
  const copyToClipboard = () => {
    if (selectedDoc?.extracted_text) {
      navigator.clipboard.writeText(selectedDoc.extracted_text);
      window.alert('Text copied to clipboard!');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'processing': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'uploaded': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (doc: Document) => {
    const dateString = doc.uploaded_at || doc.created_at;
    if (dateString) {
      return new Date(dateString).toLocaleDateString();
    }
    return '-';
  };

  const filteredDocs = documents.filter(doc =>
    doc.filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Document Library</h2>
        <div className="flex items-center space-x-4">
          <button
            onClick={async () => {
              const unprocessed = documents.filter(d => d.status === 'uploaded');
              if (unprocessed.length === 0) {
                alert('No documents to process!');
                return;
              }
              if (window.confirm(`Process ${unprocessed.length} documents?`)) {
                for (const doc of unprocessed) {
                  try {
                    await fetch(`http://localhost:8001/api/v1/process/${doc.id}`, { method: 'POST' });
                  } catch (e) {
                    console.error('Failed to process:', doc.filename);
                  }
                }
                alert(`Started processing ${unprocessed.length} documents!`);
                setTimeout(() => window.location.reload(), 2000);
              }
            }}
            className="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 flex items-center gap-2 text-sm"
            title="Process all unprocessed documents"
          >
            <Play className="h-4 w-4" />
            Process All ({documents.filter(d => d.status === 'uploaded').length})
          </button>
          <button
            onClick={() => window.open('http://localhost:8001/api/v1/documents/export/excel', '_blank')}
            className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2 text-sm"
            title="Export all documents to Excel"
          >
            <Download className="h-4 w-4" />
            Export All
          </button>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search documents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            onClick={fetchDocuments}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Refresh"
          >
            <RefreshCw className="h-5 w-5 text-gray-600" />
          </button>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded text-primary-600"
            />
            <span className="text-sm">Auto-refresh</span>
          </label>
        </div>
      </div>

      {filteredDocs.length === 0 ? (
        <div className="text-center py-12">
          <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-gray-500">
            {searchTerm ? 'No documents match your search.' : 'No documents uploaded yet.'}
          </p>
          <p className="text-sm text-gray-400 mt-2">
            Upload documents from the Upload page to see them here.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b bg-gray-50">
                <th className="text-left py-3 px-4 font-medium text-gray-700">Filename</th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">Document Type</th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">Uploaded</th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredDocs.map((doc) => {
                const docStatus = doc.status || "uploaded";
                return (
                  <tr key={doc.id} className="hover:bg-gray-50 transition-colors">
                    <td className="py-4 px-4">
                      <div className="flex items-center">
                        <FileText className="h-5 w-5 text-gray-400 mr-3" />
                        <span className="text-sm font-medium text-gray-900">
                          {doc.filename}
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className="text-sm text-gray-600">{doc.file_type}</span>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusColor(docStatus)}`}>
                        {docStatus}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <span className="text-sm text-gray-600">{doc.document_type || '-'}</span>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-500">
                      {formatDate(doc)}
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex space-x-3">
                        {docStatus === 'uploaded' && (
                          <button 
                            onClick={() => handleProcess(doc)}
                            className="text-purple-600 hover:text-purple-800 transition-colors" 
                            title="Process with OCR"
                          >
                            <Play className="h-5 w-5" />
                          </button>
                        )}
                        <button 
                          onClick={() => handleView(doc)}
                          className="text-blue-600 hover:text-blue-800 transition-colors disabled:opacity-50" 
                          title="View Document"
                          disabled={viewerLoading || docStatus !== 'completed'}
                        >
                          <Eye className="h-5 w-5" />
                        </button>
                        <button 
                          onClick={() => handleDownload(doc)}
                          className="text-green-600 hover:text-green-800 transition-colors disabled:opacity-50" 
                          title="Download Extracted Text"
                          disabled={docStatus !== 'completed'}
                        >
                          <Download className="h-5 w-5" />
                        </button>
                        <button 
                          onClick={() => handleDelete(doc)}
                          className="text-red-600 hover:text-red-800 transition-colors" 
                          title="Delete Document"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Document Viewer Modal */}
      {showViewer && selectedDoc && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-6xl h-5/6 flex flex-col">
            {/* Modal Header */}
            <div className="flex justify-between items-center p-6 border-b border-gray-200">
              <div>
                <h2 className="text-xl font-bold text-gray-900">{selectedDoc.filename}</h2>
                <p className="text-gray-600">
                  OCR Results - {selectedDoc.word_count || 0} words extracted
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    const doc = documents.find(d => d.id === selectedDoc.id);
                    if (doc && selectedDoc.extracted_text) {
                      const blob = new Blob([selectedDoc.extracted_text], { type: 'text/plain' });
                      const url = URL.createObjectURL(blob);
                      const link = document.createElement('a');
                      link.href = url;
                      link.download = `${doc.filename.replace(/\.[^/.]+$/, '')}_extracted.txt`;
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                      URL.revokeObjectURL(url);
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
                  title="Export extracted text"
                >
                  <Download className="h-4 w-4" />
                  Export TXT
                </button>
                <button
                  onClick={() => {
                    const doc = documents.find(d => d.id === selectedDoc.id);
                    if (doc && selectedDoc.extracted_text) {
                      const csvContent = `Filename,Type,Status,Confidence,Word Count,Extracted Text
"${doc.filename}","${doc.file_type}","${doc.status}","${selectedDoc.confidence}%","${selectedDoc.word_count}","${selectedDoc.extracted_text.replace(/"/g, '""').replace(/\n/g, ' ')}"`;
                      const blob = new Blob([csvContent], { type: 'text/csv' });
                      const url = URL.createObjectURL(blob);
                      const link = document.createElement('a');
                      link.href = url;
                      link.download = `${doc.filename.replace(/\.[^/.]+$/, '')}_extracted.csv`;
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                      URL.revokeObjectURL(url);
                    }
                  }}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
                >
                  <Download className="h-4 w-4" />
                  Export CSV
                </button>
                <button
                  onClick={closeViewer}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="flex-1 p-6 overflow-hidden">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
                {/* Document Stats */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900">Document Information</h3>
                  <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Word Count:</span>
                      <span className="font-medium">{selectedDoc.word_count || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Confidence:</span>
                      <span className="font-medium text-green-600">{selectedDoc.confidence || 0}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Processing Time:</span>
                      <span className="font-medium">{selectedDoc.processing_time || 0}s</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">File Size:</span>
                      <span className="font-medium">{selectedDoc.file_size || 'Unknown'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Document Type:</span>
                      <span className="font-medium">{selectedDoc.metadata?.document_type || 'Unknown'}</span>
                    </div>
                  </div>

{/* NER Entities */}
                  {entities && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <h3 className="font-semibold text-gray-900 mb-3">🤖 Extracted Entities (NER)</h3>
                      <div className="space-y-2 text-sm">
                        {entities.persons?.length > 0 && (
                          <div>
                            <span className="text-gray-700 font-medium">👤 Persons: </span>
                            {entities.persons.map((p: string, i: number) => (
                              <span key={i} className="inline-block px-2 py-1 bg-blue-100 text-blue-800 rounded mr-1 mb-1 text-xs">{p}</span>
                            ))}
                          </div>
                        )}
                        {entities.organizations?.length > 0 && (
                          <div>
                            <span className="text-gray-700 font-medium">🏢 Organizations: </span>
                            {entities.organizations.map((o: string, i: number) => (
                              <span key={i} className="inline-block px-2 py-1 bg-purple-100 text-purple-800 rounded mr-1 mb-1 text-xs">{o}</span>
                            ))}
                          </div>
                        )}
                        {entities.dates?.length > 0 && (
                          <div>
                            <span className="text-gray-700 font-medium">📅 Dates: </span>
                            {entities.dates.map((d: string, i: number) => (
                              <span key={i} className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded mr-1 mb-1 text-xs">{d}</span>
                            ))}
                          </div>
                        )}
                        {entities.locations?.length > 0 && (
                          <div>
                            <span className="text-gray-700 font-medium">📍 Locations: </span>
                            {entities.locations.map((l: string, i: number) => (
                              <span key={i} className="inline-block px-2 py-1 bg-red-100 text-red-800 rounded mr-1 mb-1 text-xs">{l}</span>
                            ))}
                          </div>
                        )}
                        {entities.money?.length > 0 && (
                          <div>
                            <span className="text-gray-700 font-medium">💰 Money: </span>
                            {entities.money.map((m: string, i: number) => (
                              <span key={i} className="inline-block px-2 py-1 bg-yellow-100 text-yellow-800 rounded mr-1 mb-1 text-xs">{m}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  )}


                  {/* Preview of Original */}
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Original Document</h4>
                    <div className="bg-gray-100 rounded-lg p-4 h-48 flex items-center justify-center">
                      <div className="text-center">
                        <FileText className="mx-auto h-12 w-12 text-gray-400 mb-2" />
                        <p className="text-gray-600">PDF Preview</p>
                        <p className="text-sm text-gray-500">{selectedDoc.filename}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Extracted Text */}
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-gray-900">Extracted Text</h3>
                    <button
                      onClick={copyToClipboard}
                      className="px-3 py-1 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                      title="Copy to clipboard"
                    >
                      <Copy className="h-4 w-4" />
                      Copy
                    </button>
                  </div>
                  <div className="bg-white border border-gray-200 rounded-lg p-4 h-96 overflow-y-auto">
                    <pre className="whitespace-pre-wrap text-sm leading-relaxed text-gray-800">
                      {selectedDoc.extracted_text || 'No extracted text available.'}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Loading overlay for viewer */}
      {viewerLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
            <span>Loading document...</span>
          </div>
        </div>
      )}
    </div>
  );
};