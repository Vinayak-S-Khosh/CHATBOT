# Vinayak S Khosh - Portfolio Website

A professional portfolio website built with Flask to showcase projects, skills, education, and certificates.

## Features

- **Home Page**: Hero section with introduction and featured projects
- **About Page**: Career objective and professional summary
- **Projects Page**: Detailed project cards with technologies and descriptions
- **Skills Page**: Technical skills organized by category with proficiency bars
- **Education Page**: Education timeline, certifications, and leadership activities
- **Certificates Page**: Display certificate images
- **Contact Page**: Contact form and social media links

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Font Awesome 6

## Project Structure

```
PORTFOLIO/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
│
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar and footer
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── projects.html     # Projects page
│   ├── skills.html       # Skills page
│   ├── education.html    # Education & certifications
│   ├── certificates.html # Certificates gallery
│   └── contact.html      # Contact page
│
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom CSS
    └── images/           # Images folder
        ├── profile.jpg   # Your profile photo
        ├── cert_1.jpg    # Certificate images
        ├── cert_2.jpg
        ├── cert_3.jpg
        ├── project_1.jpg # Project screenshots
        └── project_2.jpg
```

## Installation & Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Your Images

Place your images in the `static/images/` folder:
- `profile.jpg` - Your profile photo
- `cert_1.jpg`, `cert_2.jpg`, `cert_3.jpg` - Certificate images
- `project_1.jpg`, `project_2.jpg` - Project screenshots

### 3. Run the Application Locally

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Running on a Server

### Option 1: Using Gunicorn (Production Server - Linux)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 2: Using Waitress (Production Server - Windows)

1. Install Waitress:
```bash
pip install waitress
```

2. Create a file `serve.py`:
```python
from waitress import serve
from app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
```

3. Run:
```bash
python serve.py
```

### Option 3: Deploy to Cloud Platforms

#### Heroku
1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-portfolio-name
git push heroku main
```

#### PythonAnywhere
1. Upload your files to PythonAnywhere
2. Set up a web app with manual configuration
3. Point WSGI file to your app

#### Render.com
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`

### Option 4: VPS (DigitalOcean, AWS, etc.)

1. SSH into your server
2. Install Python and pip
3. Clone your repository
4. Install dependencies:
```bash
pip install -r requirements.txt
pip install gunicorn
```

5. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

6. (Optional) Set up Nginx as reverse proxy and SSL with Let's Encrypt

## Accessing from Other Devices on Local Network

When running locally, the app is accessible at `http://0.0.0.0:5000`, which means:
- On the same computer: `http://localhost:5000`
- From other devices on the same network: `http://YOUR_IP_ADDRESS:5000`

To find your IP address:
- Windows: `ipconfig` (look for IPv4 Address)
- Mac/Linux: `ifconfig` or `ip addr`

## Customization

### Update Personal Information

Edit `app.py` to update:
- Projects data
- Skills data
- Education data
- Certifications
- Contact information

### Change Colors/Styling

Edit `static/css/style.css` to customize:
- Color scheme (CSS variables in `:root`)
- Font sizes
- Spacing
- Animations

### Add More Pages

1. Create a new route in `app.py`
2. Create a new template in `templates/`
3. Add navigation link in `base.html`

## Security Notes

- Change `SECRET_KEY` in `app.py` before deploying
- Never commit sensitive data to Git
- Use environment variables for sensitive configuration
- Enable HTTPS in production

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available for personal use.

## Contact

Vinayak S Khosh
- Email: vinayaksunilkhosh@gmail.com
- GitHub: https://github.com/Vinayak-S-Khosh
- LinkedIn: https://www.linkedin.com/in/vinayak-sunil-khosh-2005
