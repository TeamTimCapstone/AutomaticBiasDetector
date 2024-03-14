import React, { useState } from 'react';
import './App.css'; // Adjust the CSS file as needed

function App() {
  const [generatingReport, setGeneratingReport] = useState(false);

  const handleGenerateReport = () => {
    // This function will be triggered when the button is clicked
    // You can perform other actions here as needed, such as making API calls
    setGeneratingReport(true);
    // If you're making an asynchronous call, setGeneratingReport(false)
    // should be called once the operation is complete.
  };

  return (
    <div className="App">
      <div className="body-content">
      {!generatingReport ? (
        <div className='left-side'>
          <h1>Welcome to Bias Detector</h1>
          <p>Analyze an article and receive a report of detected bias</p>
          <button className='startbutton' onClick={handleGenerateReport}>Get Started</button>
        </div>
        ) : (
          // This is the content shown when generatingReport is true
          <div className='left-side'>
            <h1>Generating Report</h1>
            <p>Please wait while we process your request...</p>
          </div>
        )}
      </div>  
    </div>
  );
}

export default App;
