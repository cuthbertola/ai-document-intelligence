import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Home, Upload, FileText } from 'lucide-react';
import { Dashboard } from './components/Dashboard';
import { FileUpload } from './components/FileUpload';
import { DocumentList } from './components/DocumentList';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Sidebar */}
        <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg">
          <div className="flex items-center justify-center h-16 bg-primary-600">
            <h1 className="text-white text-xl font-bold">Doc Intelligence</h1>
          </div>
          
          <nav className="mt-8">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 ${
                  isActive ? 'bg-gray-100 border-l-4 border-primary-600' : ''
                }`
              }
            >
              <Home className="h-5 w-5 mr-3" />
              Dashboard
            </NavLink>
            
            <NavLink
              to="/upload"
              className={({ isActive }) =>
                `flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 ${
                  isActive ? 'bg-gray-100 border-l-4 border-primary-600' : ''
                }`
              }
            >
              <Upload className="h-5 w-5 mr-3" />
              Upload
            </NavLink>
            
            <NavLink
              to="/documents"
              className={({ isActive }) =>
                `flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 ${
                  isActive ? 'bg-gray-100 border-l-4 border-primary-600' : ''
                }`
              }
            >
              <FileText className="h-5 w-5 mr-3" />
              Documents
            </NavLink>
          </nav>
        </div>

        {/* Main Content */}
        <div className="ml-64 p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<FileUpload />} />
            <Route path="/documents" element={<DocumentList />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
