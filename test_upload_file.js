// Test file for VibeCodeAuditor scanning
// This file contains intentional security issues for testing

const express = require('express');
const app = express();

// Security Issue 1: Hardcoded API key (Critical)
const API_KEY = 'sk-1234567890abcdef'; // This should be in environment variables

// Security Issue 2: SQL Injection vulnerability (High)
app.get('/user/:id', (req, res) => {
    const userId = req.params.id;
    const query = `SELECT * FROM users WHERE id = ${userId}`; // Vulnerable to SQL injection
    // Should use parameterized queries
});

// Security Issue 3: Missing input validation (Medium)
app.post('/update-profile', (req, res) => {
    const userData = req.body; // No validation
    // Should validate and sanitize input
    updateUserProfile(userData);
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});