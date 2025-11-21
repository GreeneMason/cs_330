const path = require('path');

// Simulate the same path resolution as the API
const frontendDir = "C:\\Users\\Smokable\\code\\cs_330\\cs_330\\frontend";
const scriptPath = path.join(frontendDir, '..', 'backend', 'src', 'prediction', 'predict_ensemble.py');
const pythonPath = 'C:/Users/Smokable/code/cs_330/cs_330/.venv/Scripts/python.exe';

console.log('Frontend directory:', frontendDir);
console.log('Script path:', scriptPath);
console.log('Python path:', pythonPath);

// Check if files exist
const fs = require('fs');
console.log('Script exists:', fs.existsSync(scriptPath));
console.log('Python exists:', fs.existsSync(pythonPath));