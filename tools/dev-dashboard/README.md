# UFC Prediction System - Developer Dashboard

## Overview
Real-time developer dashboard for monitoring the UFC Prediction System's frontend, backend, and overall health.

## Features
- **Service Status Monitoring**: Real-time status of frontend (Next.js) and backend (Flask)
- **System Health Metrics**: CPU, memory, disk usage, and network connections
- **Process Monitoring**: Active Node.js and Python processes
- **Activity Logging**: Real-time activity feed with timestamps
- **Performance Charts**: Visual representation of system performance over time
- **WebSocket Updates**: Live updates without page refresh

## Quick Start
```bash
# Navigate to dashboard directory
cd dev-dashboard

# Install dependencies
pip install -r requirements.txt

# Start the dashboard
python app.py
```

## Dashboard URL
Once started, access the dashboard at: **http://localhost:5001**

## Monitored Services
- **Frontend**: http://localhost:3000 (Next.js)
- **Backend**: http://localhost:8000 (Flask API)

## Dashboard Sections

### 🚀 Service Status
- Real-time status indicators for frontend/backend
- Response times and uptime tracking
- Error detection and logging

### 📊 System Health
- CPU usage percentage
- Memory usage percentage  
- Disk space utilization
- Active network connections

### ⚙️ Active Processes
- Running Node.js processes (frontend)
- Running Python processes (backend)
- Resource usage per process

### 📈 API Performance
- Request counts and success rates
- Average response times
- Error tracking

### 📋 Activity Log
- Chronological activity feed
- Service status changes
- Error notifications
- System events

### 📉 Performance Charts
- Real-time CPU and memory usage graphs
- Historical performance data
- Visual trend analysis

## Technical Details

### Architecture
- **Flask**: Web server and API endpoints
- **WebSocket**: Real-time updates via SocketIO
- **Chart.js**: Performance visualization
- **psutil**: System metrics collection

### Update Frequency
- **Real-time**: WebSocket updates every 10 seconds
- **Backup**: HTTP polling every 30 seconds
- **Charts**: Live updates with 20-point history

### Responsive Design
- Optimized for desktop development environments
- Mobile-friendly responsive layout
- Dark theme for reduced eye strain

## API Endpoints
- `GET /` - Dashboard HTML page
- `GET /api/status` - Current system status JSON
- `GET /api/logs` - Activity and error logs
- WebSocket events for real-time updates

## Security
- **Dev-only**: Intended for development environments
- **Local access**: Binds to all interfaces for team access
- **No authentication**: Assumes trusted network environment

## Troubleshooting

### Dashboard won't start
```bash
# Check if port 5001 is available
netstat -an | findstr 5001

# Install missing dependencies
pip install -r requirements.txt
```

### Services show as offline
- Ensure frontend is running on port 3000
- Ensure backend is running on port 8000
- Check firewall settings for port access

### High resource usage
- Dashboard uses minimal resources
- Monitor system processes via the dashboard
- Adjust monitoring frequency if needed