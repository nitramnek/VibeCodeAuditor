/**
 * React sample with security vulnerabilities for testing framework-specific rules.
 */

import React, { useState, useEffect } from 'react';

// Hardcoded sensitive data
const API_KEY = 'sk-1234567890abcdef';
const DATABASE_URL = 'mongodb://admin:password123@localhost:27017/myapp';

function VulnerableComponent() {
  const [userInput, setUserInput] = useState('');
  const [htmlContent, setHtmlContent] = useState('');
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    // Storing sensitive data in localStorage
    localStorage.setItem('api_key', API_KEY);
    localStorage.setItem('user_password', 'user123');
    
    // Loading user data without validation
    const storedData = localStorage.getItem('user_data');
    if (storedData) {
      setUserData(JSON.parse(storedData)); // No validation
    }
  }, []);

  const handleUserInput = (event) => {
    const input = event.target.value;
    setUserInput(input);
    
    // Dangerous: Using eval with user input
    try {
      const result = eval(input); // Extremely dangerous
      console.log('Eval result:', result);
    } catch (e) {
      console.error('Eval error:', e);
    }
  };

  const handleSubmit = () => {
    // XSS vulnerability: Direct innerHTML assignment
    document.getElementById('output').innerHTML = userInput;
    
    // Another XSS vulnerability: Using dangerouslySetInnerHTML without sanitization
    setHtmlContent(userInput);
    
    // Unsafe redirect based on user input
    if (userInput.includes('redirect:')) {
      const url = userInput.split('redirect:')[1];
      window.location = url; // Open redirect vulnerability
    }
  };

  const loadExternalContent = async () => {
    // Loading content from user-controlled URL
    const url = userInput;
    try {
      const response = await fetch(url); // SSRF vulnerability
      const data = await response.text();
      
      // Using document.write (deprecated and unsafe)
      document.write(data);
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      // No file type validation
      const reader = new FileReader();
      reader.onload = (e) => {
        // Directly executing file content
        const script = document.createElement('script');
        script.innerHTML = e.target.result; // Dangerous
        document.head.appendChild(script);
      };
      reader.readAsText(file);
    }
  };

  const authenticateUser = (username, password) => {
    // Weak authentication logic
    if (username === 'admin' && password === 'admin') {
      // Storing sensitive info in sessionStorage
      sessionStorage.setItem('isAdmin', 'true');
      sessionStorage.setItem('userRole', 'administrator');
      return true;
    }
    return false;
  };

  const makeApiCall = async () => {
    // Exposing API key in client-side code
    const headers = {
      'Authorization': `Bearer ${API_KEY}`,
      'X-API-Key': API_KEY
    };
    
    try {
      const response = await fetch('/api/data', { headers });
      const data = await response.json();
      
      // Logging sensitive data
      console.log('API Response:', data);
      console.log('Headers sent:', headers);
      
      return data;
    } catch (error) {
      // Exposing internal error details
      alert(`API Error: ${error.message}`);
    }
  };

  return (
    <div className="vulnerable-component">
      <h1>Vulnerable React Component</h1>
      
      {/* XSS vulnerability: dangerouslySetInnerHTML without sanitization */}
      <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      
      <input
        type="text"
        value={userInput}
        onChange={handleUserInput}
        placeholder="Enter some input..."
      />
      
      <button onClick={handleSubmit}>Submit (Unsafe)</button>
      <button onClick={loadExternalContent}>Load External Content</button>
      
      <input type="file" onChange={handleFileUpload} />
      
      <div id="output"></div>
      
      {/* Inline event handlers with user data */}
      <button onClick={() => eval(userInput)}>
        Execute Input (Very Dangerous)
      </button>
      
      {/* Exposing sensitive data in DOM */}
      <div style={{ display: 'none' }}>
        API Key: {API_KEY}
        Database URL: {DATABASE_URL}
      </div>
      
      {userData && (
        <div>
          {/* Potential XSS if userData contains malicious content */}
          <span dangerouslySetInnerHTML={{ __html: userData.bio }} />
        </div>
      )}
    </div>
  );
}

// Component with more vulnerabilities
function AnotherVulnerableComponent({ userContent }) {
  const [state, setState] = useState('');
  
  useEffect(() => {
    // Direct DOM manipulation instead of React patterns
    document.getElementById('direct-dom').innerHTML = userContent;
    
    // Using setTimeout with string (acts like eval)
    setTimeout(`console.log('${userContent}')`, 1000);
  }, [userContent]);

  const handleClick = () => {
    // Creating script tags dynamically
    const script = document.createElement('script');
    script.src = userContent; // User-controlled script source
    document.body.appendChild(script);
  };

  return (
    <div>
      <div id="direct-dom"></div>
      <button onClick={handleClick}>Load Script</button>
    </div>
  );
}

export default VulnerableComponent;