import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadDocument } from '../services/api';

interface UploadedFile {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  result?: any;
  error?: string;
}

export const FileUpload: React.FC = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [useAdvanced, setUseAdvanced] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      status: 'pending' as const,
    }));
    setFiles(prev => [...prev, ...newFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp'],
      'text/plain': ['.txt'],
    },
  });

  const processFiles = async () => {
    setIsUploading(true);
    
    for (let i = 0; i < files.length; i++) {
      if (files[i].status !== 'pending') continue;
      
      setFiles(prev => prev.map((f, idx) => 
        idx === i ? { ...f, status: 'uploading' } : f
      ));

      try {
        const result = await uploadDocument(files[i].file, useAdvanced);
        setFiles(prev => prev.map((f, idx) => 
          idx === i ? { ...f, status: 'success', result } : f
        ));
      } catch (error: any) {
        setFiles(prev => prev.map((f, idx) => 
          idx === i ? { ...f, status: 'error', error: error.message } : f
        ));
      }
    }
    
    setIsUploading(false);
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const clearAll = () => {
    setFiles([]);
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">Upload Documents</h2>
      
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400'}`}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        {isDragActive ? (
          <p className="text-primary-600">Drop the files here...</p>
        ) : (
          <div>
            <p className="text-gray-600">Drag & drop files here, or click to select</p>
            <p className="text-sm text-gray-500 mt-2">Supports PDF, Images (PNG, JPG, TIFF), and Text files</p>
          </div>
        )}
      </div>

      {files.length > 0 && (
        <div className="mt-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold">Files ({files.length})</h3>
            <button onClick={clearAll} className="text-red-600 hover:text-red-700 text-sm">
              Clear all
            </button>
          </div>
          
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {files.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <File className="h-5 w-5 text-gray-500" />
                  <div>
                    <p className="text-sm font-medium">{file.file.name}</p>
                    <p className="text-xs text-gray-500">
                      {(file.file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {file.status === 'pending' && (
                    <button onClick={() => removeFile(index)}>
                      <X className="h-5 w-5 text-gray-500 hover:text-red-600" />
                    </button>
                  )}
                  {file.status === 'uploading' && (
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
                  )}
                  {file.status === 'success' && (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  )}
                  {file.status === 'error' && (
                    <AlertCircle className="h-5 w-5 text-red-500" />
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 space-y-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={useAdvanced}
                onChange={(e) => setUseAdvanced(e.target.checked)}
                className="rounded text-primary-600"
              />
              <span className="text-sm">Use advanced OCR (ML-based layout analysis)</span>
            </label>
            
            <button
              onClick={processFiles}
              disabled={isUploading || files.every(f => f.status !== 'pending')}
              className="btn-primary w-full disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isUploading ? 'Processing...' : 'Process Documents'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
