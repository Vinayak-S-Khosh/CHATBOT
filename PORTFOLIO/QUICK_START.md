# Quick Start Guide - Portfolio Website

## Your Flask Portfolio is Ready! 🎉

### What's Been Created

A complete portfolio website with **7 pages**:
1. **Home** - Hero section with your introduction
2. **About** - Career objective and professional summary
3. **Projects** - Your 2 projects with details
4. **Skills** - Technical skills organized by category
5. **Education** - Education timeline and certifications
6. **Certificates** - Certificate gallery with images
7. **Contact** - Contact form and social links

---

## Running Locally (Development)

### 1. Open Terminal in Project Folder
```bash
cd d:\PORTFOLIO
```

### 2. Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python app.py
```

### 4. Open in Browser
- **Local:** http://localhost:5000
- **Network:** http://192.168.1.19:5000 (accessible from phone/tablet on same WiFi)

### 5. Stop Server
Press `Ctrl+C` in the terminal

---

## Adding Your Images

Place your images in `static/images/` folder:

### Required Files:
- `profile.jpg` - Your photo (400x400px recommended)
- `cert_1.jpg` - Web Development certificate
- `cert_2.jpg` - Cyber Security certificate  
- `cert_3.jpg` - AI & ML Orientation certificate
- `project_1.jpg` - Timetable Generator screenshot
- `project_2.jpg` - AI Chatbot screenshot

**Note:** The website works with placeholder images if you haven't added real images yet.

---

## Customizing Content

### Update Personal Info
Open `app.py` and modify:
- Projects descriptions
- Skills lists
- Contact information
- Education details

### Change Colors/Style
Edit `static/css/style.css`:
- Look for `:root` section at the top
- Change color values as needed

---

## Deploying to Internet (Free Options)

### Option 1: PythonAnywhere (Easiest)
1. Sign up: https://www.pythonanywhere.com
2. Upload files via Files tab
3. Configure web app (see DEPLOYMENT_GUIDE.md)
4. Your site: `https://YOUR_USERNAME.pythonanywhere.com`

### Option 2: Render.com (Modern)
1. Push code to GitHub
2. Sign up: https://render.com
3. Connect GitHub repo
4. Auto-deploy on every push
5. Free tier available

### Option 3: Heroku
1. Install Heroku CLI
2. Run deployment commands (see DEPLOYMENT_GUIDE.md)
3. Custom domain support

**Full deployment instructions:** See `DEPLOYMENT_GUIDE.md`

---

## Project Structure

```
PORTFOLIO/
├── app.py              # Main Flask application (routes & logic)
├── requirements.txt    # Python dependencies
├── templates/          # HTML pages
│   ├── base.html      # Base template (navbar, footer)
│   ├── index.html     # Home page
│   ├── about.html     # About page
│   ├── projects.html  # Projects page
│   ├── skills.html    # Skills page
│   ├── education.html # Education page
│   ├── certificates.html  # Certificates page
│   └── contact.html   # Contact page
└── static/
    ├── css/
    │   └── style.css  # Custom styling
    └── images/        # Your images go here
```

---

## Features Included

✅ **Responsive Design** - Works on mobile, tablet, desktop  
✅ **Modern UI** - Bootstrap 5 with custom styling  
✅ **Font Awesome Icons** - Professional icons  
✅ **Contact Form** - Opens email client  
✅ **Project Cards** - Showcase your work  
✅ **Skills Proficiency Bars** - Visual skill levels  
✅ **Social Links** - GitHub, LinkedIn, Email  
✅ **SEO Ready** - Meta tags included  
✅ **Fast Loading** - Optimized CSS and HTML  

---

## Common Tasks

### Add a New Project
Edit `app.py`, find `projects_data` and add:
```python
{
    'title': 'Your Project Name',
    'status': 'Completed',  # or 'Ongoing'
    'tech': ['Python', 'Django'],
    'description': 'Project description',
    'features': [
        'Feature 1',
        'Feature 2'
    ]
}
```

### Add More Skills
Edit `app.py`, find `skills_data` and update the dictionary.

### Change Your Info
Find `contact_info` in `app.py` and update your details.

---

## Troubleshooting

### Port 5000 Already in Use
Another program is using port 5000. Either:
- Stop the other program
- Change port in `app.py`: `app.run(port=5001)`

### Static Files Not Loading
- Check file paths
- Clear browser cache (Ctrl+F5)
- Ensure files are in correct folders

### Can't Access from Phone
- Make sure phone is on same WiFi
- Check firewall settings
- Use your computer's IP address

---

## Next Steps

1. ✅ **Add Your Images** - Replace placeholders
2. ✅ **Test All Pages** - Click through navigation
3. ✅ **Customize Content** - Update projects, skills
4. ✅ **Deploy Online** - Choose a hosting platform
5. ✅ **Share Your Portfolio** - Add to resume, LinkedIn

---

## Getting Help

**Documentation:**
- README.md - Full project overview
- DEPLOYMENT_GUIDE.md - Detailed deployment instructions

**Support:**
- Email: vinayaksunilkhosh@gmail.com
- GitHub: https://github.com/Vinayak-S-Khosh

---

## Tips for Success

💡 **Professional Photo** - Use a clear, professional headshot  
💡 **Project Screenshots** - Show your work visually  
💡 **Regular Updates** - Keep projects and skills current  
💡 **Mobile Testing** - Test on your phone before deploying  
💡 **Custom Domain** - Consider buying a domain (e.g., vinayakkhosh.com)  

---

**Your portfolio is live at:** http://localhost:5000

Click the preview button to view your website! 🚀
