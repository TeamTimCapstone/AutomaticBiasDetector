const express = require('express');
const app = express();
const cors = require('cors');
const { exec } = require('child_process');

const hostname = '172.31.4.148';
const port = 5000;

app.use(express.json());
app.use(cors());

app.post('/biasdetector', async (req, res) => {
  try {
    const { text } = req.body; // Assuming the URL is provided in the 'text' property of the request body
    console.log('Received URL:', text);

    // Construct the command to execute the Python script with the URL as an argument
    const command = `python3 bias_detector.py ${text}`;

    // Execute the command
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'An error occurred while running the algorithm' });
        return;
      }
      
      // Log the output received from the Python script
      console.log('Output from Python script:', stdout);
      
      // Assuming the Python script outputs JSON
      const jsonOutput = JSON.parse(stdout);
      
      // Send the JSON output back as the response
      res.json(jsonOutput);
    });
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
