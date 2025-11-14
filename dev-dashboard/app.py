#!/usr/bin/env python3
"""
Developer Dashboard - Real-time monitoring for UFC Prediction System
Shows frontend/backend status, API activity, and system health
"""

import os
import sys
import time
import json
import psutil
import requests
import threading
from datetime import datetime, timedelta
from collections import deque, defaultdict
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()  # Generate random secret key
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"
        self.activity_log = deque(maxlen=100)
        self.api_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0,
            'last_request': None
        }
        self.service_status = {
            'frontend': {'status': 'unknown', 'last_check': None, 'uptime': 0},
            'backend': {'status': 'unknown', 'last_check': None, 'uptime': 0}
        }
        self.system_metrics = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_usage': 0,
            'network_connections': 0
        }
        self.response_times = deque(maxlen=50)
        self.error_log = deque(maxlen=50)
        
    def log_activity(self, activity_type, message, status="info"):
        """Log system activity with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.append({
            'timestamp': timestamp,
            'type': activity_type,
            'message': message,
            'status': status
        })
        
    def check_service_health(self, service_name, url, endpoint="/health"):
        """Check if a service is responding"""
        try:
            start_time = time.time()
            response = requests.get(f"{url}{endpoint}", timeout=3)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                self.service_status[service_name].update({
                    'status': 'online',
                    'last_check': datetime.now(),
                    'response_time': response_time
                })
                return True, response_time
            else:
                self.service_status[service_name].update({
                    'status': 'error',
                    'last_check': datetime.now(),
                    'error_code': response.status_code
                })
                return False, response_time
                
        except requests.exceptions.ConnectionError:
            self.service_status[service_name].update({
                'status': 'offline',
                'last_check': datetime.now(),
                'error': 'Connection refused'
            })
            return False, None
        except requests.exceptions.Timeout:
            self.service_status[service_name].update({
                'status': 'timeout',
                'last_check': datetime.now(),
                'error': 'Request timeout'
            })
            return False, None
        except Exception as e:
            self.service_status[service_name].update({
                'status': 'error',
                'last_check': datetime.now(),
                'error': str(e)
            })
            return False, None

    def check_frontend_health(self):
        """Check Next.js frontend status"""
        try:
            # Try to reach the main page
            response = requests.get(self.frontend_url, timeout=3)
            if response.status_code == 200:
                self.service_status['frontend'].update({
                    'status': 'online',
                    'last_check': datetime.now(),
                    'framework': 'Next.js',
                    'port': 3000
                })
                return True
        except:
            pass
            
        self.service_status['frontend'].update({
            'status': 'offline',
            'last_check': datetime.now(),
            'framework': 'Next.js',
            'port': 3000
        })
        return False

    def check_backend_health(self):
        """Check Flask backend status"""
        return self.check_service_health('backend', self.backend_url)

    def get_system_metrics(self):
        """Collect system performance metrics"""
        try:
            self.system_metrics.update({
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            
            # Count network connections
            connections = psutil.net_connections()
            self.system_metrics['network_connections'] = len([c for c in connections if c.status == 'ESTABLISHED'])
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

    def get_process_info(self):
        """Get information about running Node.js and Python processes"""
        processes = {
            'node_processes': [],
            'python_processes': []
        }
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'cmdline']):
                try:
                    pinfo = proc.info
                    if 'node' in pinfo['name'].lower():
                        processes['node_processes'].append({
                            'pid': pinfo['pid'],
                            'cpu': pinfo['cpu_percent'],
                            'memory': pinfo['memory_percent'],
                            'command': ' '.join(pinfo['cmdline'][:3]) if pinfo['cmdline'] else ''
                        })
                    elif 'python' in pinfo['name'].lower():
                        cmdline = ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ''
                        if 'app.py' in cmdline or 'flask' in cmdline.lower():
                            processes['python_processes'].append({
                                'pid': pinfo['pid'],
                                'cpu': pinfo['cpu_percent'],
                                'memory': pinfo['memory_percent'],
                                'command': cmdline[:100] + '...' if len(cmdline) > 100 else cmdline
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            logger.error(f"Error getting process info: {e}")
            
        return processes

monitor = SystemMonitor()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """API endpoint to get current system status"""
    # Check services
    frontend_online = monitor.check_frontend_health()
    backend_online, backend_time = monitor.check_backend_health()
    
    # Get system metrics
    monitor.get_system_metrics()
    
    # Get process information
    processes = monitor.get_process_info()
    
    return jsonify({
        'services': monitor.service_status,
        'system': monitor.system_metrics,
        'processes': processes,
        'activity': list(monitor.activity_log)[-20:],  # Last 20 activities
        'api_metrics': monitor.api_metrics,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/logs')
def get_logs():
    """Get recent activity logs"""
    return jsonify({
        'activity_log': list(monitor.activity_log),
        'error_log': list(monitor.error_log)
    })

def background_monitoring():
    """Background task to continuously monitor services"""
    while True:
        try:
            # Check services every 10 seconds
            frontend_status = monitor.check_frontend_health()
            backend_status, _ = monitor.check_backend_health()
            
            # Log status changes
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if frontend_status:
                monitor.log_activity("frontend", "Frontend service is running", "success")
            else:
                monitor.log_activity("frontend", "Frontend service is down", "error")
                
            if backend_status:
                monitor.log_activity("backend", "Backend service is responding", "success")
            else:
                monitor.log_activity("backend", "Backend service is not responding", "error")
            
            # Update system metrics
            monitor.get_system_metrics()
            
            # Emit real-time updates via WebSocket
            socketio.emit('status_update', {
                'services': monitor.service_status,
                'system': monitor.system_metrics,
                'processes': monitor.get_process_info(),
                'timestamp': current_time
            })
            
        except Exception as e:
            logger.error(f"Background monitoring error: {e}")
            
        time.sleep(10)  # Check every 10 seconds

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connected', {'message': 'Connected to dev dashboard'})
    logger.info("Client connected to dashboard")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    logger.info("Client disconnected from dashboard")

if __name__ == '__main__':
    # Log startup
    monitor.log_activity("system", "Developer dashboard starting up", "info")
    
    # Start background monitoring thread
    monitoring_thread = threading.Thread(target=background_monitoring, daemon=True)
    monitoring_thread.start()
    
    print("\n" + "="*60)
    print("🚀 UFC PREDICTION SYSTEM - DEVELOPER DASHBOARD")
    print("="*60)
    print(f"📊 Dashboard URL: http://localhost:5001")
    print(f"🎯 Monitoring:")
    print(f"   • Frontend: http://localhost:3000")
    print(f"   • Backend:  http://localhost:8000")
    print("="*60)
    print()
    
    # Run the dashboard
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)