# 🌟 AstroCSV Web Application

A modern web application for astrological calculations with a beautiful React frontend and FastAPI backend.

## 🚀 **Features**

- **🌐 Web Interface**: Beautiful, responsive React frontend
- **🔮 Astrological Calculations**: Complete KP system with sub-lords
- **📍 Location-based**: Calculate for any coordinates worldwide
- **📅 Date-specific**: Choose any date for calculations
- **📊 Results Display**: Interactive results with degree buckets
- **📥 CSV Export**: Download complete data for analysis
- **🎨 Modern UI**: Styled with styled-components and gradients
- **📱 Responsive**: Works on desktop, tablet, and mobile

## 🏗️ **Architecture**

```
AstroCSV Web App
├── 🐍 FastAPI Backend (Port 8000)
│   ├── /calculate - Main calculation endpoint
│   ├── /degree-buckets - Generate degree buckets
│   ├── /signs - Zodiac signs information
│   ├── /nakshatras - Nakshatra information
│   └── /health - Health check
├── ⚛️ React Frontend (Port 3000)
│   ├── Header - App title and features
│   ├── AstroCalculator - Input form with presets
│   └── ResultsDisplay - Results and CSV export
└── 📁 Core Library
    ├── mapping.py - Astrological calculations
    ├── ephem.py - Astronomical calculations
    └── csvout.py - CSV generation
```

## 🛠️ **Installation & Setup**

### **Prerequisites**
- Python 3.11+
- Node.js 16+
- npm or yarn

### **1. Clone and Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd LBAT

# Activate virtual environment
source /path/to/your/venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### **2. Start the Backend (FastAPI)**
```bash
# Option 1: Use the startup script
python start_api.py

# Option 2: Direct uvicorn
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend will be available at:**
- 🌐 **API**: http://localhost:8000
- 📖 **Documentation**: http://localhost:8000/docs
- 🔍 **Interactive API**: http://localhost:8000/redoc

### **3. Start the Frontend (React)**
```bash
# Option 1: Use the startup script
python start_frontend.py

# Option 2: Manual setup
cd frontend
npm install
npm start
```

**Frontend will be available at:**
- 🌐 **Web App**: http://localhost:3000

## 🎯 **How to Use**

### **1. Web Interface**
1. **Open**: Navigate to http://localhost:3000
2. **Input**: Enter latitude, longitude, and date
3. **Calculate**: Click "Calculate Astrological Data"
4. **View Results**: See comprehensive astrological information
5. **Export**: Download CSV with complete data

### **2. API Endpoints**

#### **Calculate Astrological Data**
```bash
POST /calculate
{
  "latitude": 19.0760,
  "longitude": 72.8777,
  "date": "2025-08-20",
  "include_degree_buckets": true
}
```

#### **Get Degree Buckets**
```bash
GET /degree-buckets
```

#### **Get Zodiac Signs**
```bash
GET /signs
```

#### **Get Nakshatras**
```bash
GET /nakshatras
```

### **3. Quick Location Presets**
The web interface includes preset buttons for popular cities:
- **Indian Cities**: Mumbai, Delhi, Kolkata, Chennai, Pune, Bangalore, Hyderabad
- **International**: New York, London

## 🔧 **Development**

### **Backend Development**
```bash
# Install development dependencies
pip install fastapi uvicorn python-multipart

# Run with auto-reload
uvicorn api.main:app --reload --port 8000
```

### **Frontend Development**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### **File Structure**
```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.js          # App header
│   │   ├── AstroCalculator.js # Input form
│   │   └── ResultsDisplay.js  # Results display
│   ├── App.js                 # Main app component
│   └── index.js               # Entry point
├── public/
│   └── index.html             # HTML template
└── package.json               # Dependencies

api/
└── main.py                    # FastAPI application

start_api.py                   # Backend startup script
start_frontend.py              # Frontend startup script
```

## 🌟 **Key Components**

### **AstroCalculator Component**
- **Input Form**: Latitude, longitude, date picker
- **Preset Locations**: Quick selection for popular cities
- **Options**: Toggle for degree buckets inclusion
- **Validation**: Input validation and error handling

### **ResultsDisplay Component**
- **Results Cards**: Sunrise, ascendant, KP system
- **Degree Buckets**: Interactive table with 0.5° intervals
- **CSV Export**: Download complete dataset
- **Responsive Design**: Mobile-friendly layout

### **API Features**
- **CORS Support**: Cross-origin requests enabled
- **Input Validation**: Coordinate and date validation
- **Error Handling**: Comprehensive error responses
- **Pydantic Models**: Type-safe request/response handling

## 🎨 **Styling & UI**

- **Styled Components**: CSS-in-JS for component styling
- **Gradient Backgrounds**: Modern visual appeal
- **Responsive Grid**: Adaptive layout for all screen sizes
- **Interactive Elements**: Hover effects and animations
- **Color Scheme**: Professional astrological theme

## 📱 **Responsive Design**

- **Desktop**: Full-featured interface with all options
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface with stacked layout

## 🚀 **Deployment**

### **Production Build**
```bash
# Frontend
cd frontend
npm run build

# Backend
pip install gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### **Docker Support**
```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:16-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
CMD ["npm", "start"]
```

## 🔍 **Testing**

### **API Testing**
```bash
# Test the API
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 19.0760, "longitude": 72.8777, "date": "2025-08-20"}'
```

### **Frontend Testing**
```bash
cd frontend
npm test
```

## 📊 **Performance**

- **Backend**: FastAPI with async support
- **Frontend**: React with optimized rendering
- **Data**: Efficient degree bucket generation
- **Export**: Streamlined CSV generation

## 🔒 **Security**

- **Input Validation**: Coordinate and date validation
- **CORS Configuration**: Controlled cross-origin access
- **Error Handling**: Safe error responses
- **Data Sanitization**: Clean input processing

## 🌟 **Future Enhancements**

- **User Authentication**: Login and user profiles
- **Calculation History**: Save and retrieve past calculations
- **Advanced Charts**: Visual representation of data
- **Batch Processing**: Multiple location calculations
- **API Rate Limiting**: Usage controls and monitoring

## 🆘 **Troubleshooting**

### **Common Issues**

1. **Port Already in Use**
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   
   # Kill process using port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **Dependencies Issues**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Python Path Issues**
   ```bash
   # Ensure you're in the right directory
   pwd
   # Should show: /path/to/LBAT
   
   # Activate virtual environment
   source /path/to/venv/bin/activate
   ```

## 📞 **Support**

- **Documentation**: Check API docs at http://localhost:8000/docs
- **Issues**: Report bugs in the project repository
- **Questions**: Check the project README for CLI usage

## 🎉 **Success!**

Your AstroCSV web application is now running with:
- 🌐 **Frontend**: http://localhost:3000
- 🔗 **Backend**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs

Enjoy calculating astrological data through the beautiful web interface! 🌟
