# Deployment Guide - Flask Portfolio Website

This guide covers multiple deployment options for your Flask portfolio website.

## Quick Start (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

Your website will be available at:
- Local: http://localhost:5000
- Network: http://YOUR_IP:5000 (accessible from other devices on your network)

To find your IP:
- Windows: `ipconfig` (look for IPv4 Address)
- Mac/Linux: `ifconfig` or `hostname -I`

---

## Production Deployment Options

### Option 1: PythonAnywhere (Free & Easy)

**Best for**: Beginners, free hosting for small projects

1. **Sign up** at https://www.pythonanywhere.com (free account)

2. **Upload files**:
   - Go to "Files" tab
   - Upload all project files or clone from GitHub

3. **Install dependencies**:
   - Open Bash console
   ```bash
   pip install --user Flask==3.0.0 Werkzeug==3.0.1
   ```

4. **Configure Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10 or 3.11

5. **WSGI Configuration**:
   - Click on WSGI configuration file
   - Replace content with:
   ```python
   import sys
   path = '/home/YOUR_USERNAME/PORTFOLIO'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Reload** and visit: `https://YOUR_USERNAME.pythonanywhere.com`

---

### Option 2: Render.com (Free Tier Available)

**Best for**: Modern deployment with auto-deploy from Git

1. **Prepare files**:
   - Ensure `requirements.txt` is in root
   - Create `render.yaml` (optional):
   ```yaml
   services:
     - type: web
       name: portfolio
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app
   ```

2. **Sign up** at https://render.com

3. **Create Web Service**:
   - Connect your GitHub repository
   - Select your repository
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`

4. **Add Gunicorn**:
   - Update `requirements.txt`:
   ```
   Flask==3.0.0
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```

5. **Deploy**: Render will auto-deploy on every push

---

### Option 3: Heroku

**Best for**: Scalable applications

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Create files**:

   **Procfile** (no extension):
   ```
   web: gunicorn app:app
   ```

   **runtime.txt**:
   ```
   python-3.11.9
   ```

   Update **requirements.txt**:
   ```
   Flask==3.0.0
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```

3. **Deploy**:
   ```bash
   heroku login
   heroku create your-portfolio-name
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   heroku open
   ```

---

### Option 4: Vercel (with Serverless)

**Best for**: Fast deployment with serverless architecture

1. **Create `vercel.json`**:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

---

### Option 5: Railway

**Best for**: Simple deployment with free tier

1. **Sign up** at https://railway.app

2. **Deploy from GitHub**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configuration**:
   - Railway auto-detects Flask
   - Ensure `requirements.txt` includes gunicorn

4. **Environment Variables** (if needed):
   - Add `SECRET_KEY` in Railway dashboard

---

### Option 6: VPS (DigitalOcean, AWS, Linode)

**Best for**: Full control, production applications

#### Setup Steps:

1. **SSH into your server**:
   ```bash
   ssh root@YOUR_SERVER_IP
   ```

2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Clone your project**:
   ```bash
   cd /var/www
   git clone https://github.com/YOUR_USERNAME/portfolio.git
   cd portfolio
   ```

4. **Install Python packages**:
   ```bash
   pip3 install -r requirements.txt
   pip3 install gunicorn
   ```

5. **Create systemd service** (`/etc/systemd/system/portfolio.service`):
   ```ini
   [Unit]
   Description=Portfolio Flask App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/portfolio
   ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Start service**:
   ```bash
   sudo systemctl start portfolio
   sudo systemctl enable portfolio
   ```

7. **Configure Nginx** (`/etc/nginx/sites-available/portfolio`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/portfolio/static;
       }
   }
   ```

8. **Enable site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **SSL with Let's Encrypt**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## Using Waitress (Windows Production Server)

For Windows servers, use Waitress instead of Gunicorn:

1. **Install Waitress**:
   ```bash
   pip install waitress
   ```

2. **Create `serve.py`**:
   ```python
   from waitress import serve
   from app import app

   if __name__ == '__main__':
       serve(app, host='0.0.0.0', port=5000, threads=4)
   ```

3. **Run**:
   ```bash
   python serve.py
   ```

---

## Environment Variables (Production)

For production, use environment variables for sensitive data:

1. **Update `app.py`**:
   ```python
   import os
   
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
   ```

2. **Set environment variables**:
   - Linux: Add to `.bashrc` or `.env` file
   - Heroku/Render: Use dashboard
   - Windows: System Properties → Environment Variables

---

## Post-Deployment Checklist

- [ ] Change SECRET_KEY in production
- [ ] Test all pages and navigation
- [ ] Upload profile photo and images
- [ ] Test contact form
- [ ] Verify mobile responsiveness
- [ ] Check SSL certificate (HTTPS)
- [ ] Set up custom domain (if applicable)
- [ ] Add Google Analytics (optional)
- [ ] Test on multiple browsers
- [ ] Set up monitoring/logging

---

## Monitoring & Maintenance

### Error Logging
Add logging to `app.py`:
```python
import logging

if not app.debug:
    logging.basicConfig(filename='error.log', level=logging.ERROR)
```

### Uptime Monitoring
- Use: UptimeRobot, Pingdom, or StatusCake
- Set up alerts for downtime

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux
sudo lsof -i :5000
kill -9 <PID>
```

### Static Files Not Loading
- Check `static/` folder structure
- Verify file paths in templates
- Clear browser cache

### 500 Internal Server Error
- Check application logs
- Verify all dependencies installed
- Check file permissions

---

## Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Deployment Guide: https://flask.palletsprojects.com/en/3.0.x/deploying/
- Gunicorn Docs: https://docs.gunicorn.org/

---

## Support

For issues or questions:
- Email: vinayaksunilkhosh@gmail.com
- GitHub: https://github.com/Vinayak-S-Khosh
