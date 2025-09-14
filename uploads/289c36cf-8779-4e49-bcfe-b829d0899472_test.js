// insecure_app.js
// WARNING: this file is intentionally bad practice and insecure.
// Do NOT use in production.

const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());

// 1) Permissive CORS (allows any origin)
app.use(cors());

// 2) Hard-coded credentials and secret in source code
const DB_USER = 'admin';
const DB_PASS = 'changeme123';            // <-- hard-coded secret
const JWT_SECRET = 'supersecretjwtkey';   // <-- hard-coded secret

// 3) Verbose error messages returned to clients (leaks internal info)
function errorHandler(err, req, res, next) {
    console.error('Full stack:', err.stack);               // logs stack to console
    res.status(500).json({ error: err.message, stack: err.stack }); // returns stack trace
}
app.use(errorHandler);

// 4) No authentication on sensitive endpoint
app.get('/admin/config', (req, res) => {
    res.json({
        dbUser: DB_USER,
        dbPass: DB_PASS,            // leaking credentials via API
        jwtSecret: JWT_SECRET
    });
});

// 5) Insecure token creation (no expiry, weak claims)
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username === DB_USER && password === DB_PASS) {
        // token with no expiration
        const token = jwt.sign({ sub: username, role: 'admin' }, JWT_SECRET);
        res.json({ token });
    } else {
        res.status(401).json({ error: 'invalid credentials' });
    }
});

// 6) Storing logs containing PII in plaintext files without access control
app.post('/submit', (req, res) => {
    // suppose req.body contains PII (full name, national id)
    fs.appendFileSync('./app_logs.txt', JSON.stringify(req.body) + '\n'); // no encryption
    res.json({ ok: true });
});

// 7) No input validation => possible injection risk
app.post('/search', (req, res) => {
    // imagine this runs a DB query constructed by concatenation (not shown)
    const q = req.body.q;
    // pretend we run a DB query with q directly
    res.json({ results: `Pretend results for ${q}` });
});

app.listen(3000, () => console.log('Insecure app running on 3000'));
