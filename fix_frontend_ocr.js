// Fix for DocumentList.tsx to properly handle OCR processing

const fs = require('fs');
const path = require('path');

const documentListPath = path.join('/Users/olawalebadekale/ai-document-platform/src/components/documents/DocumentList.tsx');

let content = fs.readFileSync(documentListPath, 'utf8');

// Find and update the handleProcess function
const updatedHandleProcess = `
  const handleProcess = async (documentId: number, filename: string) => {
    setProcessingDocuments(prev => new Set(prev).add(documentId));
    
    try {
      // For PDF files, use the OCR processing endpoint
      if (filename.endsWith('.pdf')) {
        // First, get the file from the backend
        const downloadResponse = await fetch(\`http://localhost:8000/api/v1/documents/\${documentId}/download\`);
        if (!downloadResponse.ok) throw new Error('Failed to download document');
        
        const blob = await downloadResponse.blob();
        const file = new File([blob], filename, { type: 'application/pdf' });
        
        // Create FormData and send to OCR endpoint
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('http://localhost:8000/api/ocr/process', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) throw new Error('OCR processing failed');
        
        const result = await response.json();
        
        // Update the document status
        setDocuments(prev => prev.map(doc => 
          doc.id === documentId 
            ? { ...doc, status: 'completed', word_count: result.word_count }
            : doc
        ));
        
        // Show success message
        alert(\`Document processed successfully! \${result.word_count} words extracted.\`);
      } else {
        // For non-PDF files, just mark as completed
        setDocuments(prev => prev.map(doc => 
          doc.id === documentId 
            ? { ...doc, status: 'completed' }
            : doc
        ));
      }
    } catch (error) {
      console.error('Processing error:', error);
      alert('Failed to process document. Please try again.');
      
      // Reset status on error
      setDocuments(prev => prev.map(doc => 
        doc.id === documentId 
          ? { ...doc, status: 'uploaded' }
          : doc
      ));
    } finally {
      setProcessingDocuments(prev => {
        const newSet = new Set(prev);
        newSet.delete(documentId);
        return newSet;
      });
    }
  };`;

// Replace the handleProcess function
const processRegex = /const handleProcess = async[\s\S]*?^\s*};/m;
if (processRegex.test(content)) {
  content = content.replace(processRegex, updatedHandleProcess);
} else {
  console.log('Could not find handleProcess function, adding it...');
  // Add it before the return statement
  const returnIndex = content.indexOf('return (');
  content = content.slice(0, returnIndex) + updatedHandleProcess + '\n\n' + content.slice(returnIndex);
}

fs.writeFileSync(documentListPath, content);
console.log('✅ Fixed DocumentList.tsx OCR processing');
