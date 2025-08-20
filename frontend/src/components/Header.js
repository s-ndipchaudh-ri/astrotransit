import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const HeaderContent = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
`;

const Title = styled.h1`
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  margin: 0;
  opacity: 0.8;
  font-size: 1rem;
`;

const SidebarToggle = styled.button`
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
  }
`;

const ToggleIcon = styled.span`
  font-size: 1.2rem;
`;

const Header = ({ onToggleSidebar, showSidebar }) => {
  return (
    <HeaderContainer>
      <HeaderContent>
        <div>
          <Title>🌟 LBAT AstroCSV</Title>
          <Subtitle>Astrological Calculations & Data Export</Subtitle>
        </div>
      </HeaderContent>
      <SidebarToggle onClick={onToggleSidebar}>
        <ToggleIcon>{showSidebar ? '◀' : '▶'}</ToggleIcon>
        {showSidebar ? 'Hide' : 'Show'} Sidebar
      </SidebarToggle>
    </HeaderContainer>
  );
};

export default Header;
