const express = require('express');
const app = express();
const cors = require('cors');
const { PythonShell } = require('python-shell');

//const { get_bias_info } = require('./bias_detector.py'); // Provide the correct path to bias_detector.py

const hostname = '172.31.4.148';
const port = 5000;

app.use(express.json()); // Add this line to parse JSON request bodies
app.use(cors());

app.post('/biasdetector', async (req, res) => {
  try {
    const article_url = req.body;
    console.log(req.body);
    console.log(article_url);
    const pyScriptPath = './bias_detector.py';
    const functionName = 'get_bias_info';
    const parameters = [article_url];

    // Run the Python script asynchronously
    const output = await PythonShell
      .run(pyScriptPath, { args: [functionName, ...parameters] });

    const jsonOutput = JSON.parse(output[0]);

    // Send the result back as the response
    res.json(jsonOutput);
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
