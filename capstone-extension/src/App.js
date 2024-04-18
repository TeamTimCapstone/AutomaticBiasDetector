import React, { useState } from 'react';
import './App.css';

/* global chrome */

function App() {
  const [splitView, setSplitView] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [report, setReport] = useState('');
  const [reportGenerated, setReportGenerated] = useState(false);

  const toggleSplitView = () => {
    setSplitView(!splitView);
  };

  const handleGenerateReport = async () => {
    setGeneratingReport(true);
    chrome.tabs.query({active: true, currentWindow: true}, async (tabs) => {
      const currentTabUrl = tabs[0].url; // Get URL of the current active tab

      try {
        const response = await fetch('http://3.142.197.82:5000/biasdetector', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: currentTabUrl })
        });

        if (!response.ok) {
          throw new Error('Failed to generate report');
        }

        const data = await response.json();
        setReport(data);
        setReportGenerated(true);
      } catch (error) {
        console.error('Error:', error.message);
        setReportGenerated(false);
      }
      setGeneratingReport(false);
      toggleSplitView(); // Activate split view after fetching the report
    });
  };

  return (
    <div className="App">
      <div className={`body-content ${splitView || generatingReport ? 'split-view' : ''}`}>
        <div className='left-side'>
          <h1>Welcome to Bias Detector</h1>
          <p>Analyze an article and receive a report of detected bias</p>
          {!generatingReport ? (
            <button className='startbutton' onClick={handleGenerateReport}>Get Started</button>
          ) : (
            <div className="loading-screen">
              <h2>Generating Report</h2>
              <p>Please wait...</p>
            </div>
          )}
        </div>
        {splitView && (
          <div className='right-side'>
            <button className="close-button" onClick={toggleSplitView}>X</button>
            {!reportGenerated ? (
              <div className="loading-screen">
                <h2>Processing...</h2>
                <p>Please wait as we generate your report.</p>
              </div>
            ) : report && (
              <div>
                <h2>Report Generated</h2>
                <p>Label: {report.label}</p>
                <p>Article URL: <a href={report.article_url}>{report.article_url}</a></p>
                <p>Article Bias Confidence: {report.article_bias_confidence}</p>
                <p>Biased Sentence Count: {report.biased_sentence_count}</p>
                <h3>Biased Sentences:</h3>
                <ul>
                  {report.bias_info_by_sentence.map((sentence, index) => (
                    <li key={index}>
                      <p>Sentence: {sentence.text}</p>
                      <p>Sentence Bias Confidence: {sentence.sentence_bias_confidence}</p>
                      {sentence.biased_words && (
                        <p>Biased Words: {sentence.biased_words.join(', ')}</p>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
