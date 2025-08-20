import React, { useState } from 'react';
import styled from 'styled-components';

const SidebarContainer = styled.div`
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const SidebarHeader = styled.div`
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
`;

const SidebarTitle = styled.h3`
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SidebarSubtitle = styled.p`
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
`;

const ResultsList = styled.div`
  flex: 1;
  overflow-y: auto;
`;

const ResultItem = styled.div`
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    border-color: #667eea;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
  }
  
  ${props => props.active && `
    border-color: #667eea;
    background: #f0f4ff;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
  `}
`;

const ResultDate = styled.div`
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 8px;
`;

const ResultLocation = styled.div`
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 8px;
`;

const ResultDetails = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  font-size: 0.8rem;
`;

const DetailItem = styled.div`
  display: flex;
  flex-direction: column;
`;

const DetailLabel = styled.span`
  color: #6c757d;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.7rem;
`;

const DetailValue = styled.span`
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.8rem;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
`;

const EmptyIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
`;

const EmptyText = styled.p`
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
`;

const ClearButton = styled.button`
  background: #dc3545;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s ease;
  width: 100%;
  margin-top: 15px;
  
  &:hover {
    background: #c82333;
  }
`;

const Sidebar = ({ dateRangeResults, onSelectResult, onClearResults, currentResultIndex = 0 }) => {
  const handleResultClick = (result, index) => {
    onSelectResult(result);
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    const date = new Date(timeString);
    return date.toLocaleDateString('en-IN', {
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  };

  if (dateRangeResults.length === 0) {
    return (
      <SidebarContainer>
        <SidebarHeader>
          <SidebarTitle>📊 Results Sidebar</SidebarTitle>
          <SidebarSubtitle>View your calculation results here</SidebarSubtitle>
        </SidebarHeader>
        <EmptyState>
          <EmptyIcon>📋</EmptyIcon>
          <EmptyText>
            No results yet. <br />
            Run a calculation to see results here.
          </EmptyText>
        </EmptyState>
      </SidebarContainer>
    );
  }

  return (
    <SidebarContainer>
      <SidebarHeader>
        <SidebarTitle>📊 Results Sidebar</SidebarTitle>
        <SidebarSubtitle>
          {dateRangeResults.length} calculation{dateRangeResults.length !== 1 ? 's' : ''} available
        </SidebarSubtitle>
      </SidebarHeader>

      <ResultsList>
        {dateRangeResults.map((result, index) => (
          <ResultItem
            key={index}
            active={index === currentResultIndex}
            onClick={() => handleResultClick(result, index)}
          >
            <ResultDate>
              📅 {formatTime(result.date)}
            </ResultDate>
            <ResultLocation>
              📍 {result.latitude}°N, {result.longitude}°E
            </ResultLocation>
            <ResultDetails>
              <DetailItem>
                <DetailLabel>Date</DetailLabel>
                <DetailValue>{formatTime(result.date)}</DetailValue>
              </DetailItem>
              <DetailItem>
                <DetailLabel>Time</DetailLabel>
                <DetailValue>{result.sunrise ? new Date(result.sunrise).toLocaleTimeString('en-IN', {hour: '2-digit', minute: '2-digit'}) : 'N/A'}</DetailValue>
              </DetailItem>
              <DetailItem>
                <DetailLabel>Ascendant</DetailLabel>
                <DetailValue>{result.ascendant}° {result.ascendant_sign}</DetailValue>
              </DetailItem>
              <DetailItem>
                <DetailLabel>Sub Lord</DetailLabel>
                <DetailValue>{result.ascendant_sub_lord}</DetailValue>
              </DetailItem>
            </ResultDetails>
          </ResultItem>
        ))}
      </ResultsList>

      <ClearButton onClick={onClearResults}>
        🗑️ Clear All Results
      </ClearButton>
    </SidebarContainer>
  );
};

export default Sidebar;
