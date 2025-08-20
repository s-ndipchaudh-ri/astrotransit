import React, { useState } from 'react';
import styled from 'styled-components';

const ResultsContainer = styled.div`
  padding: 30px;
  background: white;
  flex: 1;
`;

const ResultsHeader = styled.div`
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
  text-align: center;
`;

const ResultsTitle = styled.h2`
  margin: 0 0 10px 0;
  font-size: 1.8rem;
`;

const ResultsSubtitle = styled.p`
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
`;

const ResultsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const ResultCard = styled.div`
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
`;

const CardTitle = styled.h3`
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const CardIcon = styled.span`
  font-size: 1.5rem;
`;

const InfoGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
`;

const InfoItem = styled.div`
  display: flex;
  flex-direction: column;
`;

const InfoLabel = styled.span`
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const InfoValue = styled.span`
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 600;
  margin-top: 2px;
`;

const DegreeBucketsSection = styled.div`
  margin-top: 30px;
`;

const BucketsHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
`;

const BucketsTitle = styled.h3`
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
`;

const BucketsControls = styled.div`
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
`;

const ToggleButton = styled.button`
  background: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s ease;
  
  &:hover {
    background: #5a6fd8;
  }
`;

const SearchInput = styled.input`
  padding: 8px 12px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 200px;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
  }
`;

const BucketsTable = styled.div`
  max-height: 500px;
  overflow-y: auto;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const TableHeader = styled.div`
  display: grid;
  grid-template-columns: 60px 80px 80px 80px 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 10px;
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  position: sticky;
  top: 0;
  z-index: 10;
`;

const TableRow = styled.div`
  display: grid;
  grid-template-columns: 60px 80px 80px 80px 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 10px;
  padding: 12px 15px;
  border-bottom: 1px solid #f1f3f4;
  font-size: 0.9rem;
  background: ${props => {
    if (props.isSubSubLordChange) return '#fff3cd';
    if (props.isSubLordChange) return '#e8f5e8';
    if (props.isNakshatraLordChange) return '#e3f2fd';
    return 'transparent';
  }};
  border-left: ${props => {
    if (props.isSubSubLordChange) return '4px solid #ffc107';
    if (props.isSubLordChange) return '4px solid #28a745';
    if (props.isNakshatraLordChange) return '4px solid #17a2b8';
    return 'none';
  }};
  
  &:nth-child(even) {
    background: ${props => {
      if (props.isSubSubLordChange) return '#fff3cd';
      if (props.isSubLordChange) return '#e8f5e8';
      if (props.isNakshatraLordChange) return '#e3f2fd';
      return '#f8f9fa';
    }};
  }
  
  &:hover {
    background: ${props => {
      if (props.isSubSubLordChange) return '#ffeaa7';
      if (props.isSubLordChange) return '#d4edda';
      if (props.isNakshatraLordChange) return '#bee5eb';
      return '#e9ecef';
    }};
  }
`;

const ExportSection = styled.div`
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  text-align: center;
`;

const ExportButton = styled.button`
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(231, 76, 60, 0.3);
  }
`;

const PaginationInfo = styled.div`
  text-align: center;
  margin-top: 15px;
  color: #6c757d;
  font-size: 0.9rem;
`;

const NoResults = styled.div`
  text-align: center;
  padding: 40px;
  color: #6c757d;
`;

const NoResultsIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
`;

const DateSelectContainer = styled.div`
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

const DateSelectLabel = styled.label`
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  white-space: nowrap;
`;

const DateSelect = styled.select`
  padding: 10px 12px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  min-width: 250px;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
  }
  
  &:hover {
    border-color: #adb5bd;
  }
`;

const DateInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 0.9rem;
  color: #6c757d;
  
  span {
    display: flex;
    align-items: center;
    gap: 5px;
  }
`;



const SearchContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
  flex-wrap: wrap;
`;

const SearchResults = styled.div`
  font-size: 0.9rem;
  color: #6c757d;
  margin-left: 10px;
`;

const PaginationContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  flex-wrap: wrap;
  gap: 10px;
`;

const PaginationButton = styled.button`
  padding: 8px 12px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  background: white;
  color: #2c3e50;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s ease, border-color 0.2s ease;
  
  &:hover {
    background: #f8f9fa;
    border-color: #adb5bd;
  }
  
  &:disabled {
    background: #f8f9fa;
    border-color: #e9ecef;
    color: #adb5bd;
    cursor: not-allowed;
  }
`;

const PaginationButtons = styled.div`
  display: flex;
  gap: 10px;
`;

const AdvancedSearchSection = styled.div`
  margin: 30px 0;
  padding: 25px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
`;

const AdvancedSearchTitle = styled.h3`
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  text-align: center;
`;

const AdvancedSearchForm = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const SearchFieldGroup = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
`;

const SearchField = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const SearchLabel = styled.label`
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
`;

const AdvancedSearchInput = styled.input`
  padding: 10px 12px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
  }
  
  &:hover {
    border-color: #adb5bd;
  }
`;

const SearchButtonGroup = styled.div`
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 10px;
`;

const SearchButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ClearButton = styled.button`
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(108, 117, 125, 0.3);
  }
`;

const AdvancedSearchResults = styled.div`
  margin: 30px 0;
  padding: 25px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
`;

const AdvancedSearchResultsTitle = styled.h3`
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  text-align: center;
`;

const AdvancedSearchCriteria = styled.div`
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  text-align: center;
`;

const AdvancedSearchTable = styled.div`
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const AdvancedSearchTableHeader = styled.div`
  display: grid;
  grid-template-columns: 60px 80px 80px 80px 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 10px;
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
`;

const AdvancedSearchTableRow = styled.div`
  display: grid;
  grid-template-columns: 60px 80px 80px 80px 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 10px;
  padding: 12px 15px;
  border-bottom: 1px solid #f1f3f4;
  font-size: 0.9rem;
  
  &:nth-child(even) {
    background: #f8f9fa;
  }
  
  &:hover {
    background: #e9ecef;
  }
`;

const ResultsDisplay = ({ results, dateRangeResults = [], currentResultIndex = 0, onResultChange }) => {
  const [showBuckets, setShowBuckets] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [advancedSearch, setAdvancedSearch] = useState({
    nakshatra: '',
    nakshatra_lord: '',
    sub_lord: '',
    sub_sub_lord: '',
    sign: '',
    sign_lord: ''
  });
  const [advancedSearchResults, setAdvancedSearchResults] = useState(null);
  const [isAdvancedSearching, setIsAdvancedSearching] = useState(false);
  const itemsPerPage = 100;



  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    const date = new Date(timeString);
    return date.toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Enhanced function to detect all types of changes
  const detectChanges = (changes) => {
    if (!changes || changes.length < 2) return changes;
    
    const enhancedChanges = [...changes];
    
    for (let i = 0; i < enhancedChanges.length; i++) {
      const change = enhancedChanges[i];
      const prevChange = i > 0 ? enhancedChanges[i - 1] : null;
      
      // Initialize change flags
      change.isSubSubLordChange = false;
      change.isSubLordChange = false;
      change.isNakshatraLordChange = false;
      change.previousSubSubLord = null;
      change.previousSubLord = null;
      change.previousNakshatraLord = null;
      
      if (prevChange) {
        // Check Sub Sub Lord change
        if (change.sub_sub_lord !== prevChange.sub_sub_lord) {
          change.isSubSubLordChange = true;
          change.previousSubSubLord = prevChange.sub_sub_lord;
        }
        
        // Check Sub Lord change
        if (change.sub_lord !== prevChange.sub_lord) {
          change.isSubLordChange = true;
          change.previousSubLord = prevChange.sub_lord;
        }
        
        // Check Nakshatra Lord change
        if (change.nakshatra_lord !== prevChange.nakshatra_lord) {
          change.isNakshatraLordChange = true;
          change.previousNakshatraLord = prevChange.nakshatra_lord;
        }
      }
    }
    
    return enhancedChanges;
  };

  const filteredChanges = results.ascendant_changes 
    ? detectChanges(results.ascendant_changes).filter(change => 
        change.degree.toString().includes(searchTerm) ||
        change.ascendant_degree.toString().includes(searchTerm) ||
        change.date.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.time.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.sign.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.nakshatra.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.sign_lord.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.nakshatra_lord.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.sub_lord.toLowerCase().includes(searchTerm.toLowerCase()) ||
        change.sub_sub_lord.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  const totalPages = Math.ceil(filteredChanges.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentChanges = filteredChanges.slice(startIndex, endIndex);

  const exportToCSV = () => {
    if (!results.ascendant_changes) return;

    const headers = [
      'Degree', 'Date', 'Time', 'Ascendant', 'Sign', 'Sign Lord', 'Nakshatra', 'Nakshatra Lord', 'Sub Lord', 'Sub Sub Lord'
    ];

    const csvContent = [
      headers.join(','),
      ...results.ascendant_changes.map(change => [
        change.degree,
        change.date,
        change.time,
        change.ascendant_degree,
        change.sign,
        change.sign_lord,
        change.nakshatra,
        change.nakshatra_lord,
        change.sub_lord,
        change.sub_sub_lord
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ascendant_changes_${results.date}_${results.latitude}_${results.longitude}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const calculateCSVSize = () => {
    if (!results.ascendant_changes) return '0 KB';
    
    const headers = [
      'Degree', 'Date', 'Time', 'Ascendant', 'Sign', 'Sign Lord', 'Nakshatra', 'Nakshatra Lord', 'Sub Lord', 'Sub Sub Lord'
    ];

    const csvContent = [
      headers.join(','),
      ...results.ascendant_changes.map(change => [
        change.degree,
        change.date,
        change.time,
        change.ascendant_degree,
        change.sign,
        change.sign_lord,
        change.nakshatra,
        change.nakshatra_lord,
        change.sub_lord,
        change.sub_sub_lord
      ].join(','))
    ].join('\n');

    const sizeInBytes = new Blob([csvContent]).size;
    const sizeInKB = (sizeInBytes / 1024).toFixed(1);
    const sizeInMB = (sizeInBytes / (1024 * 1024)).toFixed(2);
    
    if (sizeInBytes < 1024) {
      return `${sizeInBytes} B`;
    } else if (sizeInBytes < 1024 * 1024) {
      return `${sizeInKB} KB`;
    } else {
      return `${sizeInMB} MB`;
    }
  };



  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1); // Reset to first page when searching
  };

  const goToPage = (page) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)));
  };

  const handleAdvancedSearch = async () => {
    // Check if any search criteria is provided
    const hasSearchCriteria = Object.values(advancedSearch).some(value => value.trim() !== '');
    
    if (!hasSearchCriteria) {
      alert('Please enter at least one search criteria');
      return;
    }

    setIsAdvancedSearching(true);
    try {
      // Build query parameters
      const params = new URLSearchParams();
      Object.entries(advancedSearch).forEach(([key, value]) => {
        if (value.trim()) {
          params.append(key, value.trim());
        }
      });

      const response = await fetch(`/search-astrological?${params.toString()}`);
      if (response.ok) {
        const data = await response.json();
        setAdvancedSearchResults(data);
      } else {
        throw new Error('Search failed');
      }
    } catch (error) {
      console.error('Advanced search error:', error);
      alert('Search failed. Please try again.');
    } finally {
      setIsAdvancedSearching(false);
    }
  };

  const handleClearAdvancedSearch = () => {
    setAdvancedSearch({
      nakshatra: '',
      nakshatra_lord: '',
      sub_lord: '',
      sub_sub_lord: '',
      sign: '',
      sign_lord: ''
    });
    setAdvancedSearchResults(null);
  };

  return (
    <ResultsContainer>
      {dateRangeResults.length > 1 && (
        <DateSelectContainer>
          <DateSelectLabel htmlFor="dateSelect">Select Date:</DateSelectLabel>
          <DateSelect
            id="dateSelect"
            value={dateRangeResults[currentResultIndex]?.date || ''}
            onChange={(e) => {
              const selectedDate = e.target.value;
              const index = dateRangeResults.findIndex(
                (result) => result.date === selectedDate
              );
              if (index !== -1) {
                onResultChange && onResultChange(dateRangeResults[index], index);
              }
            }}
          >
            <option value="">Select a date...</option>
            {dateRangeResults.map((result, index) => (
              <option key={index} value={result.date}>
                {new Date(result.date).toLocaleDateString('en-IN', {
                  weekday: 'short',
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric'
                })} - {result.latitude.toFixed(2)}°, {result.longitude.toFixed(2)}°
              </option>
            ))}
          </DateSelect>
          <DateInfo>
            <span>
              <strong>Latitude:</strong> {results.latitude.toFixed(2)}°N
            </span>
            <span>
              <strong>Longitude:</strong> {results.longitude.toFixed(2)}°E
            </span>
          </DateInfo>
        </DateSelectContainer>
      )}



      {results.ascendant_changes && (
        <DegreeBucketsSection>
          <BucketsHeader>
            <BucketsTitle>📊 Ascendant Sub Sub Lord Changes</BucketsTitle>
            <BucketsControls>
              <SearchInput
                type="text"
                placeholder="Search Sub Sub Lord changes, degrees, dates, times, signs, nakshatras, lords..."
                value={searchTerm}
                onChange={handleSearch}
              />
              <ToggleButton onClick={() => setShowBuckets(!showBuckets)}>
                {showBuckets ? 'Hide' : 'Show'} Changes
              </ToggleButton>
            </BucketsControls>
          </BucketsHeader>

          {showBuckets && (
            <>
              {filteredChanges.length === 0 ? (
                <NoResults>
                  <NoResultsIcon>🔍</NoResultsIcon>
                  <p>No changes found for "{searchTerm}"</p>
                  <p>Try a different search term</p>
                </NoResults>
              ) : (
                <>
                  <BucketsTable>
                    <TableHeader>
                      <div>Degree</div>
                      <div>Date</div>
                      <div>Time</div>
                      <div>Ascendant</div>
                      <div>Sign</div>
                      <div>Sign Lord</div>
                      <div>Nakshatra</div>
                      <div>Nakshatra Lord</div>
                      <div>Sub Lord</div>
                      <div>Sub Sub Lord</div>
                    </TableHeader>
                    {currentChanges.map((change, index) => (
                      <TableRow 
                        key={startIndex + index} 
                        isSubSubLordChange={change.isSubSubLordChange}
                        isSubLordChange={change.isSubLordChange}
                        isNakshatraLordChange={change.isNakshatraLordChange}
                      >
                        <div>{change.degree}°</div>
                        <div>{change.date}</div>
                        <div>{change.time}</div>
                        <div>{change.ascendant_degree}°</div>
                        <div>{change.sign}</div>
                        <div>{change.sign_lord}</div>
                        <div>{change.nakshatra}</div>
                        <div>{change.nakshatra_lord}</div>
                        <div>{change.sub_lord}</div>
                        <div>
                          {change.isSubSubLordChange && change.previousSubSubLord && (
                            <span style={{ 
                              fontSize: '0.8rem', 
                              color: 'red', 
                              fontWeight: 'bold',
                              display: 'block',
                              marginBottom: '2px'
                            }}>
                              {change.previousSubSubLord} →
                            </span>
                          )}
                          <span style={{ 
                            fontWeight: change.isSubSubLordChange ? 'bold' : 'normal',
                            color: change.isSubSubLordChange ? '#28a745' : 'inherit'
                          }}>
                            {change.sub_sub_lord}
                          </span>
                        </div>
                      </TableRow>
                    ))}
                  </BucketsTable>
                  
                  {totalPages > 1 && (
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'center', 
                      gap: '10px', 
                      marginTop: '20px',
                      flexWrap: 'wrap'
                    }}>
                      <button
                        onClick={() => goToPage(currentPage - 1)}
                        disabled={currentPage === 1}
                        style={{
                          padding: '8px 12px',
                          border: '1px solid #e9ecef',
                          borderRadius: '6px',
                          background: currentPage === 1 ? '#f8f9fa' : 'white',
                          cursor: currentPage === 1 ? 'not-allowed' : 'pointer'
                        }}
                      >
                        Previous
                      </button>
                      
                      {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                        const page = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + i;
                        return (
                          <button
                            key={page}
                            onClick={() => goToPage(page)}
                            style={{
                              padding: '8px 12px',
                              border: '1px solid #e9ecef',
                              borderRadius: '6px',
                              background: page === currentPage ? '#667eea' : 'white',
                              color: page === currentPage ? 'white' : '#2c3e50',
                              cursor: 'pointer'
                            }}
                          >
                            {page}
                          </button>
                        );
                      })}
                      
                      <button
                        onClick={() => goToPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        style={{
                          padding: '8px 12px',
                          border: '1px solid #e9ecef',
                          borderRadius: '6px',
                          background: currentPage === totalPages ? '#f8f9fa' : 'white',
                          cursor: currentPage === totalPages ? 'not-allowed' : 'pointer'
                        }}
                      >
                        Next
                      </button>
                    </div>
                  )}
                  
                  <PaginationInfo>
                    Showing {startIndex + 1}-{Math.min(endIndex, filteredChanges.length)} of {filteredChanges.length} changes
                    {searchTerm && ` (filtered from ${results.ascendant_changes.length} total)`}
                  </PaginationInfo>
                </>
              )}
            </>
          )}
        </DegreeBucketsSection>
      )}

      {results.ascendant_changes && results.ascendant_changes.length > 0 && (
        <>
          {advancedSearchResults && (
            <div style={{ 
              textAlign: 'center', 
              padding: '15px', 
              background: '#e3f2fd', 
              borderRadius: '8px', 
              marginBottom: '20px',
              border: '1px solid #2196f3'
            }}>
              🔍 <strong>Advanced Search Active</strong> - Showing {advancedSearchResults.total_results} results. 
              Use the "Close Results" button above to return to the main data.
            </div>
          )}
          
          <AdvancedSearchSection>
            <AdvancedSearchTitle>🔍 Advanced Astrological Search</AdvancedSearchTitle>
            <AdvancedSearchForm>
              <SearchFieldGroup>
                <SearchField>
                  <SearchLabel>Nakshatra:</SearchLabel>
                  <AdvancedSearchInput
                    type="text"
                    placeholder="e.g., Rohini, Ashwini"
                    value={advancedSearch.nakshatra}
                    onChange={(e) => setAdvancedSearch(prev => ({ ...prev, nakshatra: e.target.value }))}
                  />
                </SearchField>
                <SearchField>
                  <SearchLabel>Nakshatra Lord:</SearchLabel>
                  <AdvancedSearchInput
                    type="text"
                    placeholder="e.g., Moon, Ketu"
                    value={advancedSearch.nakshatra_lord}
                    onChange={(e) => setAdvancedSearch(prev => ({ ...prev, nakshatra_lord: e.target.value }))}
                  />
                </SearchField>
                <SearchField>
                  <SearchLabel>Sub Lord:</SearchLabel>
                  <AdvancedSearchInput
                    type="text"
                    placeholder="e.g., Venus, Sun"
                    value={advancedSearch.sub_lord}
                    onChange={(e) => setAdvancedSearch(prev => ({ ...prev, sub_lord: e.target.value }))}
                  />
                </SearchField>
                <SearchField>
                  <SearchLabel>Sub Sub Lord:</SearchLabel>
                  <AdvancedSearchInput
                    type="text"
                    placeholder="e.g., Mars, Rahu"
                    value={advancedSearch.sub_sub_lord}
                    onChange={(e) => setAdvancedSearch(prev => ({ ...prev, sub_sub_lord: e.target.value }))}
                  />
                </SearchField>
                <SearchField>
                  <SearchLabel>Sign:</SearchLabel>
                  <AdvancedSearchInput
                    type="text"
                    placeholder="e.g., Aries, Taurus"
                    value={advancedSearch.sign}
                    onChange={(e) => setAdvancedSearch(prev => ({ ...prev, sign: e.target.value }))}
                  />
                </SearchField>
                <SearchField>
                  <SearchLabel>Sign Lord:</SearchLabel>
                  <AdvancedSearchInput
                    type="text"
                    placeholder="e.g., Mars, Venus"
                    value={advancedSearch.sign_lord}
                    onChange={(e) => setAdvancedSearch(prev => ({ ...prev, sign_lord: e.target.value }))}
                  />
                </SearchField>
              </SearchFieldGroup>
              <SearchButtonGroup>
                <SearchButton onClick={handleAdvancedSearch} disabled={isAdvancedSearching}>
                  {isAdvancedSearching ? '🔍 Searching...' : '🔍 Search'}
                </SearchButton>
                <ClearButton onClick={handleClearAdvancedSearch}>
                  🗑️ Clear
                </ClearButton>
              </SearchButtonGroup>
            </AdvancedSearchForm>
          </AdvancedSearchSection>

          {advancedSearchResults && (
            <AdvancedSearchResults>
              <AdvancedSearchResultsTitle>
                🔍 Search Results ({advancedSearchResults.total_results} found)
                <ToggleButton 
                  onClick={() => setAdvancedSearchResults(null)}
                  style={{ 
                    marginLeft: '15px', 
                    padding: '8px 16px', 
                    fontSize: '0.9rem',
                    background: '#6c757d'
                  }}
                >
                  ✕ Close Results
                </ToggleButton>
              </AdvancedSearchResultsTitle>
              <AdvancedSearchCriteria>
                <strong>Search Criteria:</strong>
                {Object.entries(advancedSearchResults.search_criteria).map(([key, value]) => 
                  value && (
                    <span key={key} style={{ 
                      background: '#e3f2fd', 
                      padding: '4px 8px', 
                      borderRadius: '4px', 
                      margin: '0 5px',
                      fontSize: '0.9rem'
                    }}>
                      {key}: {value}
                    </span>
                  )
                )}
              </AdvancedSearchCriteria>
              
              {advancedSearchResults.results.length > 0 ? (
                <AdvancedSearchTable>
                  <AdvancedSearchTableHeader>
                    <div>Degree</div>
                    <div>Date</div>
                    <div>Time</div>
                    <div>Ascendant</div>
                    <div>Sign</div>
                    <div>Sign Lord</div>
                    <div>Nakshatra</div>
                    <div>Nakshatra Lord</div>
                    <div>Sub Lord</div>
                    <div>Sub Sub Lord</div>
                  </AdvancedSearchTableHeader>
                  {advancedSearchResults.results.map((result, index) => (
                    <AdvancedSearchTableRow key={index}>
                      <div>{result.degree}°</div>
                      <div>{result.date}</div>
                      <div>{result.time}</div>
                      <div>{result.ascendant_degree}°</div>
                      <div>{result.sign}</div>
                      <div>{result.sign_lord}</div>
                      <div>{result.nakshatra}</div>
                      <div>{result.nakshatra_lord}</div>
                      <div>{result.sub_lord}</div>
                      <div>{result.sub_sub_lord}</div>
                    </AdvancedSearchTableRow>
                  ))}
                </AdvancedSearchTable>
              ) : (
                <NoResults>
                  <p>No results found for the specified criteria.</p>
                  <p>Try adjusting your search terms.</p>
                </NoResults>
              )}
            </AdvancedSearchResults>
          )}
        </>
      )}

      {results.ascendant_changes && results.ascendant_changes.length > 0 && (
        <>
          <SearchContainer>
            <SearchInput
              type="text"
              placeholder="Search Sub Sub Lord changes, degrees, dates, times, signs, nakshatras, lords..."
              value={searchTerm}
              onChange={handleSearch}
            />
            <SearchResults>
              Showing {filteredChanges.length} of {results.ascendant_changes ? results.ascendant_changes.length : 0} changes
            </SearchResults>
          </SearchContainer>

                        {filteredChanges.length > 0 ? (
                <>
                  <BucketsTable>
                    <TableHeader>
                      <div>Degree</div>
                      <div>Date</div>
                      <div>Time</div>
                      <div>Ascendant</div>
                      <div>Sign</div>
                      <div>Sign Lord</div>
                      <div>Nakshatra</div>
                      <div>Nakshatra Lord</div>
                      <div>Sub Lord</div>
                      <div>Sub Sub Lord</div>
                    </TableHeader>
                    {currentChanges.map((change, index) => (
                      <TableRow 
                        key={startIndex + index} 
                        isSubSubLordChange={change.isSubSubLordChange}
                        isSubLordChange={change.isSubLordChange}
                        isNakshatraLordChange={change.isNakshatraLordChange}
                      >
                        <div>{change.degree}°</div>
                        <div>{change.date}</div>
                        <div>{change.time}</div>
                        <div>{change.ascendant_degree}°</div>
                        <div>{change.sign}</div>
                        <div>{change.sign_lord}</div>
                        <div>{change.nakshatra}</div>
                        <div>{change.nakshatra_lord}</div>
                        <div>{change.sub_lord}</div>
                        <div>
                          {change.isSubSubLordChange && change.previousSubSubLord && (
                            <span style={{ 
                              fontSize: '0.8rem', 
                              color: 'red', 
                              fontWeight: 'bold',
                              display: 'block',
                              marginBottom: '2px'
                            }}>
                              {change.previousSubSubLord} →
                            </span>
                          )}
                          <span style={{ 
                            fontWeight: change.isSubSubLordChange ? 'bold' : 'normal',
                            color: change.isSubSubLordChange ? '#28a745' : 'inherit'
                          }}>
                            {change.sub_sub_lord}
                          </span>
                        </div>
                      </TableRow>
                    ))}
                  </BucketsTable>

                  <PaginationContainer>
                    <PaginationInfo>
                      Page {currentPage} of {totalPages} ({filteredChanges.length} total changes)
                    </PaginationInfo>
                    <PaginationButtons>
                      <PaginationButton
                        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                        disabled={currentPage === 1}
                      >
                        ← Previous
                      </PaginationButton>
                      <PaginationButton
                        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                        disabled={currentPage === totalPages}
                      >
                        Next →
                      </PaginationButton>
                    </PaginationButtons>
                  </PaginationContainer>
                </>
              ) : (
                <NoResults>
                  <p>No changes found for "{searchTerm}"</p>
                  <p>Try adjusting your search terms or check the spelling.</p>
                </NoResults>
              )}

          <ExportSection>
            <div style={{ marginBottom: '15px' }}>
              <p style={{ margin: '0 0 5px 0', color: '#6c757d', fontSize: '0.9rem' }}>
                📊 Ascendant Sub Sub Lord Changes CSV:
              </p>
              <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                gap: '20px', 
                fontSize: '0.9rem',
                color: '#2c3e50'
              }}>
                                  <span><strong>Rows:</strong> {results.ascendant_changes ? results.ascendant_changes.length + 1 : 1}</span>
                <span><strong>Columns:</strong> 10</span>
                <span><strong>File Size:</strong> {calculateCSVSize()}</span>
              </div>
            </div>
            
            <ExportButton onClick={exportToCSV}>
              📥 Export to CSV
            </ExportButton>
            
            <p style={{ marginTop: '10px', color: '#6c757d' }}>
              Download complete data with ascendant Sub Sub Lord changes, signs, nakshatras, and KP system details
            </p>
          </ExportSection>
        </>
      )}
    </ResultsContainer>
  );
};

export default ResultsDisplay;