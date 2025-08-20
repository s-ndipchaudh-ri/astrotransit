import React, { useState } from 'react';
import styled from 'styled-components';
import AstroCalculator from './components/AstroCalculator';
import ResultsDisplay from './components/ResultsDisplay';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import './App.css';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const MainContent = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  min-height: 80vh;
`;

const ContentArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const SidebarArea = styled.div`
  width: 350px;
  background: #f8f9fa;
  border-left: 1px solid #e9ecef;
  overflow-y: auto;
`;

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dateRangeResults, setDateRangeResults] = useState([]);
  const [showSidebar, setShowSidebar] = useState(false);

  const handleCalculation = async (calculationData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(calculationData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
      
      // Add to date range results if it's a single date calculation
      if (!calculationData.end_date) {
        setDateRangeResults(prev => [data, ...prev.slice(0, 9)]); // Keep last 10 results
      }
    } catch (err) {
      setError(err.message);
      console.error('Calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeCalculation = async (calculationData) => {
    setLoading(true);
    setError(null);
    
    try {
      const startDate = new Date(calculationData.start_date);
      const endDate = new Date(calculationData.end_date);
      const results = [];
      
      for (let date = new Date(startDate); date <= endDate; date.setDate(date.getDate() + 1)) {
        const dateStr = date.toISOString().split('T')[0];
        const response = await fetch('/calculate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ...calculationData,
            date: dateStr,
            end_date: undefined
          }),
        });

        if (response.ok) {
          const data = await response.json();
          results.push(data);
        }
      }
      
      setDateRangeResults(results);
      setResults(results[0]); // Show first result in main view
    } catch (err) {
      setError(err.message);
      console.error('Date range calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  return (
    <AppContainer>
      <MainContent>
        <ContentArea>
          <Header onToggleSidebar={toggleSidebar} showSidebar={showSidebar} />
          <AstroCalculator 
            onCalculate={handleCalculation} 
            onDateRangeCalculate={handleDateRangeCalculation}
            loading={loading} 
          />
          {error && (
            <div style={{ 
              padding: '20px', 
              margin: '20px', 
              backgroundColor: '#fee', 
              color: '#c33', 
              borderRadius: '10px',
              border: '1px solid #fcc'
            }}>
              <strong>Error:</strong> {error}
            </div>
          )}
          {results && <ResultsDisplay 
            results={results} 
            dateRangeResults={dateRangeResults}
            currentResultIndex={dateRangeResults.findIndex(r => r === results)}
            onResultChange={(result, index) => setResults(result)}
          />}
        </ContentArea>
        {showSidebar && (
          <SidebarArea>
            <Sidebar 
              dateRangeResults={dateRangeResults}
              onSelectResult={setResults}
              onClearResults={() => setDateRangeResults([])}
              currentResultIndex={dateRangeResults.findIndex(r => r === results)}
            />
          </SidebarArea>
        )}
      </MainContent>
    </AppContainer>
  );
}

export default App;
