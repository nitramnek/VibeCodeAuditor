// Test JavaScript file with security vulnerabilities

// Hardcoded credentials
const API_KEY = "sk-1234567890abcdef";
const PASSWORD = "admin123";
const SECRET = "my-secret-key";

// XSS vulnerability - innerHTML usage
function updateContent(userInput) {
    document.getElementById('content').innerHTML = userInput; // XSS risk
}

// Dangerous eval usage
function executeCode(code) {
    eval(code); // Very dangerous
}

// SQL injection pattern (in comments for detection)
function getUserData(userId) {
    // This would be vulnerable: SELECT * FROM users WHERE id = ${userId}
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    return query;
}

// Insecure random
function generateToken() {
    return Math.random().toString(36); // Should use crypto.getRandomValues
}

// Hardcoded database connection
const DB_CONNECTION = "mongodb://admin:password123@localhost:27017/mydb";

// More security issues
const config = {
    apiKey: "AKIAIOSFODNN7EXAMPLE",
    secretKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    password: "supersecret123"
};

console.log("This file contains intentional security vulnerabilities for testing");