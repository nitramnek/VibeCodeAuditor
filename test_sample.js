// Test JavaScript file with security issues

const password = "secret123";
const apiKey = "abc-def-123";

// XSS vulnerability
function updateContent(userInput) {
    document.getElementById("content").innerHTML = userInput;
}

// Eval usage
function executeCode(code) {
    eval(code);
}

console.log("Test JavaScript file");