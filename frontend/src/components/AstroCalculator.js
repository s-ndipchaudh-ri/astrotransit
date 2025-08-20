import React, { useState } from 'react';
import styled from 'styled-components';

const CalculatorContainer = styled.div`
  padding: 30px;
  background: #f8f9fa;
`;

const Form = styled.form`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  font-weight: 600;
  margin-bottom: 8px;
  color: #2c3e50;
  font-size: 0.9rem;
`;

const Input = styled.input`
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const DateInput = styled.input`
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  min-width: 200px;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &:hover {
    border-color: #adb5bd;
  }
`;

const CheckboxGroup = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const Checkbox = styled.input`
  margin: 0;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 15px;
  grid-column: 1 / -1;
  justify-content: center;
  flex-wrap: wrap;
`;

const Button = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-width: 200px;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const DateRangeButton = styled(Button)`
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  
  &:hover:not(:disabled) {
    box-shadow: 0 10px 20px rgba(39, 174, 96, 0.3);
  }
`;

const LoadingSpinner = styled.div`
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 10px;
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;



const CalculationModeToggle = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 10px;
  border: 1px solid #e9ecef;
  flex-wrap: wrap;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

const ToggleButton = styled.button`
  background: ${props => props.active ? '#667eea' : '#f8f9fa'};
  color: ${props => props.active ? 'white' : '#2c3e50'};
  border: 1px solid #dee2e6;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
  
  &:hover {
    background: ${props => props.active ? '#5a6fd8' : '#e9ecef'};
    transform: translateY(-1px);
  }
`;

const LocationSelect = styled.select`
  padding: 12px 16px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  min-width: 220px;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &:hover {
    border-color: #adb5bd;
  }
`;

const LocationSelectLabel = styled.label`
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  margin-right: 8px;
  white-space: nowrap;
`;



const DateSelectLabel = styled.label`
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  margin-right: 8px;
  white-space: nowrap;
`;

const LocationSelectContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
`;

const DateSelectContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
`;

const ShowBucketsToggle = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  flex-shrink: 0;
`;

const ToggleSwitch = styled.label`
  position: relative;
  display: inline-block;
  width: 52px;
  height: 26px;
  background: ${props => props.checked ? '#667eea' : '#ccc'};
  border-radius: 26px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:after {
    content: '';
    position: absolute;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    top: 2px;
    left: ${props => props.checked ? '28px' : '2px'};
    background: white;
    transition: left 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }
  
  &:hover {
    transform: scale(1.05);
  }
`;

const ToggleInput = styled.input`
  opacity: 0;
  width: 0;
  height: 0;
`;

const ToggleLabel = styled.span`
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
  white-space: nowrap;
`;

const AstroCalculator = ({ onCalculate, onDateRangeCalculate, loading }) => {
  const [calculationMode, setCalculationMode] = useState('single'); // 'single' or 'range'
  const [formData, setFormData] = useState({
    latitude: '',
    longitude: '',
    date: new Date(),
    start_date: new Date(),
    end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
    include_degree_buckets: true
  });

  const presetLocations = [
    { name: 'Kalyan', lat: 19.2433, lon: 73.1305 },
    { name: 'Dombivali', lat: 19.2167, lon: 73.0833 },
    { name: 'Shivaji Nagar (Pune)', lat: 18.5291, lon: 73.8564 },
    { name: 'Wakad (Pune)', lat: 18.5991, lon: 73.7625 },
    { name: 'Hadapsar (Pune)', lat: 18.4967, lon: 73.8578 },
    { name: 'Lonavala', lat: 18.7546, lon: 73.4062 },
    { name: 'Mumbai', lat: 19.0760, lon: 72.8777 },
    { name: 'Katraj (Pune)', lat: 18.4528, lon: 73.8654 }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleDateChange = (date, field = 'date') => {
    setFormData(prev => ({ ...prev, [field]: date }));
  };



  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.latitude || !formData.longitude) {
      alert('Please enter both latitude and longitude');
      return;
    }

    if (calculationMode === 'range') {
      if (formData.start_date >= formData.end_date) {
        alert('End date must be after start date');
        return;
      }
    }

    const calculationData = {
      latitude: parseFloat(formData.latitude),
      longitude: parseFloat(formData.longitude),
      date: formData.date.toISOString().split('T')[0],
      start_date: formData.start_date.toISOString().split('T')[0],
      end_date: formData.end_date.toISOString().split('T')[0],
      include_degree_buckets: formData.include_degree_buckets
    };

    if (calculationMode === 'single') {
      onCalculate(calculationData);
    } else {
      onDateRangeCalculate(calculationData);
    }
  };

  return (
    <CalculatorContainer>
      <CalculationModeToggle>
        <ToggleButton
          active={calculationMode === 'single'}
          onClick={() => setCalculationMode('single')}
        >
          📅 Single Date
        </ToggleButton>
        <ToggleButton
          active={calculationMode === 'range'}
          onClick={() => setCalculationMode('range')}
        >
          📊 Date Range
        </ToggleButton>
        
        <LocationSelectContainer>
          <LocationSelectLabel>📍 Location:</LocationSelectLabel>
          <LocationSelect
            value={formData.latitude && formData.longitude ? `${formData.latitude},${formData.longitude}` : ""}
            onChange={(e) => {
              if (e.target.value) {
                const [lat, lon] = e.target.value.split(',').map(Number);
                setFormData(prev => ({ ...prev, latitude: lat, longitude: lon }));
              }
            }}
          >
            <option value="">Select a location...</option>
            {presetLocations.map((location, index) => (
              <option key={index} value={`${location.lat},${location.lon}`}>
                {location.name} ({location.lat.toFixed(4)}, {location.lon.toFixed(4)})
              </option>
            ))}
          </LocationSelect>
        </LocationSelectContainer>

        <DateSelectContainer>
          <DateSelectLabel>📅 Date:</DateSelectLabel>
          <DateInput
            type="date"
            value={formData.date.toISOString().split('T')[0]}
            onChange={(e) => handleDateChange(new Date(e.target.value))}
          />
        </DateSelectContainer>



        <ShowBucketsToggle>
          <ToggleLabel>📊 Show 0.5° Buckets:</ToggleLabel>
          <ToggleInput
            type="checkbox"
            name="include_degree_buckets"
            checked={formData.include_degree_buckets}
            onChange={handleInputChange}
          />
          <ToggleSwitch checked={formData.include_degree_buckets} />
          <span style={{ fontSize: '0.8rem', color: '#6c757d', marginLeft: '8px' }}>
            (720 rows)
          </span>
        </ShowBucketsToggle>
      </CalculationModeToggle>

      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label>Latitude (°)</Label>
          <Input
            type="number"
            name="latitude"
            value={formData.latitude}
            onChange={handleInputChange}
            step="0.000001"
            placeholder="e.g., 19.0760"
            required
          />
        </FormGroup>

        <FormGroup>
          <Label>Longitude (°)</Label>
          <Input
            type="number"
            name="longitude"
            value={formData.longitude}
            onChange={handleInputChange}
            step="0.000001"
            placeholder="e.g., 72.8777"
            required
          />
        </FormGroup>

        {calculationMode === 'range' && (
          <>
            <FormGroup>
              <Label>Start Date</Label>
              <Input
                type="date"
                value={formData.start_date.toISOString().split('T')[0]}
                onChange={(e) => handleDateChange(new Date(e.target.value), 'start_date')}
              />
            </FormGroup>

            <FormGroup>
              <Label>End Date</Label>
              <Input
                type="date"
                value={formData.end_date.toISOString().split('T')[0]}
                onChange={(e) => handleDateChange(new Date(e.target.value), 'end_date')}
              />
            </FormGroup>
          </>
        )}

        <ButtonGroup>
          {calculationMode === 'single' ? (
            <Button type="submit" disabled={loading}>
              {loading && <LoadingSpinner />}
              {loading ? 'Calculating...' : 'Calculate Astrological Data'}
            </Button>
          ) : (
            <DateRangeButton type="submit" disabled={loading}>
              {loading && <LoadingSpinner />}
              {loading ? 'Calculating...' : 'Calculate Date Range'}
            </DateRangeButton>
          )}
        </ButtonGroup>
      </Form>
    </CalculatorContainer>
  );
};

export default AstroCalculator;
