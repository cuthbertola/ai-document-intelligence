import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, CheckCircle, Clock, AlertCircle } from 'lucide-react';

const API_URL = "http://localhost:8001";


export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    totalDocuments: 0,
    processedToday: 0,
    averageConfidence: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/v1/documents?limit=1000`);
        const docs = response.data.documents;
        
        const today = new Date().toDateString();
        const processedToday = docs.filter((d: any) => 
          new Date(d.uploaded_at).toDateString() === today
        ).length;
        
        const avgConf = docs.length > 0 
          ? (docs.reduce((sum: number, d: any) => sum + (d.confidence || 0), 0) / docs.length)
          : 0;
        
        setStats({
          totalDocuments: docs.length,
          processedToday: processedToday,
          averageConfidence: parseFloat(avgConf.toFixed(1)),
        });
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };
    
    fetchStats();
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Document Intelligence Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Documents</p>
              <p className="text-2xl font-bold">{stats.totalDocuments}</p>
            </div>
            <FileText className="h-8 w-8 text-primary-500" />
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Processed Today</p>
              <p className="text-2xl font-bold">{stats.processedToday}</p>
            </div>
            <Clock className="h-8 w-8 text-green-500" />
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Avg Confidence</p>
              <p className="text-2xl font-bold">{stats.averageConfidence}%</p>
            </div>
            <CheckCircle className="h-8 w-8 text-blue-500" />
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">OCR Status</p>
              <p className="text-lg font-semibold text-green-600">Online</p>
            </div>
            <AlertCircle className="h-8 w-8 text-green-500" />
          </div>
        </div>
      </div>
    </div>
  );
};
