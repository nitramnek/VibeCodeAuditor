import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { AuthProvider } from './contexts/AuthContext';
import DynamicLayout from './components/Layout/DynamicLayout';
import ErrorBoundary from './components/ErrorBoundary';
import Results from './pages/Results';
import ScanResults from './pages/ScanResults';
import Compliance from './pages/Compliance';
import Dashboard from './pages/Dashboard';

import Scanner from './pages/Scanner';
import LoginForm from './components/Auth/LoginForm';
import SignupForm from './components/Auth/SignupForm';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Router>
            <DynamicLayout>
              <Routes>
              {/* Public routes */}
              <Route path="/login" element={<LoginForm />} />
              <Route path="/signup" element={<SignupForm />} />
              
              {/* Protected routes */}
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/results/:scanId" 
                element={
                  <ProtectedRoute>
                    <Results />
                  </ProtectedRoute>
                } 
              />
              
              {/* Additional protected routes */}
              <Route
                path="/scanner"
                element={
                  <ProtectedRoute>
                    <Scanner />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/scan-results"
                element={
                  <ProtectedRoute>
                    <ScanResults />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/compliance"
                element={
                  <ProtectedRoute>
                    <Compliance />
                  </ProtectedRoute>
                }
              />

              <Route 
                path="/history" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/rules" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/team" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/integrations" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/settings" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              
              {/* Default redirect */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </DynamicLayout>
          </Router>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;