# Quick Reference Guide

Fast lookup for common commands and configurations.

## 🚀 Quick Commands

### Start Backend
```bash
# Windows
run_backend.bat

# Linux/macOS
chmod +x run_backend.sh
./run_backend.sh

# Manual
cd backend
python main.py
```

### Start Frontend
```bash
cd frontend
python -m http.server 8080
```

### Access Application
- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## 📦 Installation

### First Time Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend (no setup needed, just open index.html)
```

### Reinstall Dependencies
```bash
cd backend
pip install --upgrade -r requirements.txt
```

### Clear Cache
```bash
# Python
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Browser
# Press Ctrl+Shift+Delete or Cmd+Shift+Delete
```

---

## 🔧 Configuration

### Change API URL (Frontend)
Edit `frontend/assets/js/app.js`:
```javascript
const API_BASE_URL = 'http://your-server:8000';
```

### Change Backend Port
Edit `backend/main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Change this
    )
```

### Change Max File Size (Frontend)
Edit `frontend/assets/js/app.js`:
```javascript
const maxSize = 10 * 1024 * 1024; // 10MB
```

### Change Model Path
Edit `backend/utils/model_loader.py`:
```python
model_path = "/path/to/your/model.h5"
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```

### Module Not Found Error
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Verify Python path
which python  # Linux/macOS
where python  # Windows
```

### CORS Error
Backend CORS is already configured. If still getting errors:
1. Check backend is running
2. Verify API URL in frontend
3. Check browser console (F12)

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Try verbose mode
python -u main.py  # Windows
python3 -u main.py  # Linux/macOS
```

### Model File Not Found
```bash
# Navigate to backend
cd backend

# Check if models directory exists
ls models  # Linux/macOS
dir models  # Windows

# If not, create it
mkdir models
# Then place model file: models/mango_leaf_disease_MobileNetV2_model.h5
```

---

## 📊 API Endpoints Reference

### POST /api/predict
**Upload image for prediction**
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "accept: application/json" \
  -F "file=@image.jpg"
```

### GET /api/health
**Check API health**
```bash
curl http://localhost:8000/api/health
```

### GET /api/classes
**Get available disease classes**
```bash
curl http://localhost:8000/api/classes
```

### GET /
**API root information**
```bash
curl http://localhost:8000/
```

### GET /info
**Detailed API information**
```bash
curl http://localhost:8000/info
```

---

## 📱 Browser Developer Tools

### View Console Errors
1. Press `F12` (or `Ctrl+Shift+I`)
2. Click "Console" tab
3. Look for red errors

### Check Network Requests
1. Press `F12`
2. Click "Network" tab
3. Upload image
4. Look for `/api/predict` request
5. Check status code (should be 200)
6. View response body

### Clear Cache
1. Press `Ctrl+Shift+Delete` (or `Cmd+Shift+Delete`)
2. Select "Cached images and files"
3. Click Clear

---

## 🔐 Security Settings

### Enable HTTPS
Edit `backend/main.py`:
```python
import ssl
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/path/to/cert.crt', '/path/to/key.key')
```

### Restrict CORS Origins
Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Add Rate Limiting
```bash
pip install slowapi
```

---

## 📈 Performance Tuning

### Increase Workers
```bash
cd backend
gunicorn -w 8 -b 0.0.0.0:8000 main:app  # 8 workers
```

### Reduce Image Size Limit
Edit `frontend/assets/js/app.js`:
```javascript
const maxSize = 2 * 1024 * 1024; // 2MB
```

### Enable Caching
Add to `backend/main.py`:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_function():
    # Implementation
    pass
```

---

## 🗂️ File Locations

### Model File
```
backend/models/mango_leaf_disease_MobileNetV2_model.h5
```

### Frontend Code
```
frontend/assets/js/app.js
```

### Backend Code
```
backend/main.py
backend/routers/predict.py
backend/utils/preprocess.py
backend/utils/model_loader.py
```

### Logs (if configured)
```
backend/logs/app.log
/var/log/nginx/error.log  # Linux
```

### Configuration
```
backend/main.py  # Backend config
frontend/assets/js/app.js  # Frontend config
.env  # Environment variables (optional)
```

---

## 📚 Useful Commands

### Check Backend Status
```bash
curl http://localhost:8000/api/health
```

### View Swagger UI
```
http://localhost:8000/docs
```

### Check Port Usage
```bash
# Linux/macOS
netstat -tuln | grep 8000

# Windows
netstat -ano | findstr :8000
```

### Kill Process on Port
```bash
# Linux/macOS
kill -9 $(lsof -t -i :8000)

# Windows
taskkill /F /IM python.exe
```

### View Running Processes
```bash
# Linux/macOS
ps aux | grep python

# Windows
tasklist | findstr python
```

### Test File Upload
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -F "file=@test_image.jpg"
```

---

## 🔄 Git Commands (if using version control)

```bash
# Initialize repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Add remote
git remote add origin <repository-url>

# Push to remote
git push -u origin main
```

---

## 📦 Backup & Restore

### Backup Important Files
```bash
# Backup model
cp backend/models/mango_leaf_disease_MobileNetV2_model.h5 backup_model.h5

# Backup entire project
zip -r mango-disease-backup.zip .
```

### Restore from Backup
```bash
# Restore specific file
cp backup_model.h5 backend/models/mango_leaf_disease_MobileNetV2_model.h5

# Restore entire project
unzip mango-disease-backup.zip
```

---

## 🌐 Network Configuration

### Allow Remote Access
Edit `backend/main.py`:
```python
uvicorn.run(
    app,
    host="0.0.0.0",  # Remote access
    port=8000
)
```

### Access from Remote Machine
```bash
http://server-ip:8000
http://server-ip:8080  # Frontend (if running)
```

### Port Forwarding
```bash
# SSH tunnel
ssh -L 8000:localhost:8000 user@server-ip
```

---

## 🧪 Testing

### Test Backend
```bash
pytest backend/  # If tests are added
```

### Test Image Upload
```bash
python -c "
import requests
files = {'file': open('test.jpg', 'rb')}
response = requests.post('http://localhost:8000/api/predict', files=files)
print(response.json())
"
```

### Test API Response Time
```bash
time curl http://localhost:8000/api/health
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Project overview |
| SETUP_GUIDE.md | Installation instructions |
| DEPLOYMENT_GUIDE.md | Production deployment |
| COMPLETION_SUMMARY.md | What's included |
| QUICK_REFERENCE.md | This file |
| backend/README.md | Backend documentation |
| frontend/README.md | Frontend documentation |

---

## 💡 Tips & Tricks

### Speed Up Development
```bash
# Use auto-reload
uvicorn main:app --reload

# Watch for changes
npm install -g live-server  # Frontend live reload
```

### Debug Mode
```bash
# Export debug flag
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development  # Windows

# Or in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Empty System Cache
```bash
# Linux
sync; echo 3 > /proc/sys/vm/drop_caches

# macOS
purge

# Windows
net stop WuauServ
```

---

## ⚡ Emergency Commands

### Kill All Python Processes
```bash
# Linux/macOS
killall python

# Windows
taskkill /IM python.exe /F
```

### Reset Everything
```bash
cd backend
rm -rf venv
rm -rf __pycache__
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Clear All Logs
```bash
rm -rf backend/logs/*.log
```

---

## 📞 Quick Support

### Common Error Messages

| Error | Solution |
|-------|----------|
| Port in use | Kill process: `lsof -i :8000` |
| Module not found | Reinstall: `pip install -r requirements.txt` |
| CORS error | Check API URL in frontend |
| Model not found | Place in `backend/models/` |
| Image too large | Max 5MB, compress image |

---

## 🎯 One-Line Commands

```bash
# Start everything
cd backend && python main.py & cd ../frontend && python -m http.server 8080

# Test API
curl http://localhost:8000/api/health

# Check port
lsof -i :8000 || netstat -ano | findstr :8000

# Clean Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall from scratch
rm -rf venv && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

---

## 📚 References

- FastAPI Docs: https://fastapi.tiangolo.com
- TensorFlow: https://www.tensorflow.org
- MDN Web Docs: https://developer.mozilla.org
- Python Docs: https://docs.python.org

---

**Quick Reference v1.0** | Last Updated: March 2024
