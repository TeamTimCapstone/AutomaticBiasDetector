
const express = require('express');
const app = express();
const cors = require('cors');
const { spawn } = require('child_process');
const axios = require('axios'); // Import axios for making HTTP requests

const hostname = '0.0.0.0';
const port = 5000;

app.use(express.json());
app.use(cors());

function runPythonScript(articleText) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['./bias_detection.py'], { stdio: ['pipe', 'pipe', process.stderr] });

    // Handle stdout data from the Python script
    pythonProcess.stdout.on('data', (data) => {
      resolve(data.toString());
    });

    // Handle errors or script exit
    pythonProcess.on('error', (error) => {
        reject(error);
        });
    pythonProcess.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Python script exited with code ${code}`));
      }
    });

    // Pass input data to the Python script through stdin
    pythonProcess.stdin.write(articleText);
    pythonProcess.stdin.end();
  });
}

app.post('/biasdetector', async (req, res) => {
  const { text } = req.body; // Extract the URL from query parameters
  
  try {
    // Fetch article content from the URL
    //const articleResponse = await axios.get(url);
    //const articleText = articleResponse.data;

    // Call the function to run the Python script with the received article text
    const output = await runPythonScript(text);

    // Send the result back as the response
    res.json({ result: output });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'An error occurred while running the algorithm' });
  }
});

app.get('/', (req, res) => {
  res.send('Server running');
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
