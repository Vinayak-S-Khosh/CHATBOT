from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session, jsonify
import os
import json
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['ADMIN_PASSWORD'] = 'admin123'  # Change this to a strong password!

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CERTIFICATES_FILE = os.path.join(DATA_DIR, 'certificates.json')
SKILLS_FILE = os.path.join(DATA_DIR, 'skills.json')

# Initialize data files if they don't exist
def init_data_files():
    if not os.path.exists(CERTIFICATES_FILE):
        default_certs = [
            {'id': 1, 'name': 'Web Development', 'issuer': 'Elewayte'},
            {'id': 2, 'name': 'Cyber Security Add-on Certification', 'issuer': 'Tech By Heart'},
            {'id': 3, 'name': 'AI & ML Orientation', 'issuer': 'Technovalley'}
        ]
        with open(CERTIFICATES_FILE, 'w') as f:
            json.dump(default_certs, f, indent=2)
    
    if not os.path.exists(SKILLS_FILE):
        default_skills = {
            'programming': ['Python', 'PHP'],
            'database': ['MySQL'],
            'web': ['HTML', 'CSS'],
            'ai_ml': ['NLP (Basics)'],
            'tools': ['Git', 'Canva'],
            'other': ['APIs', 'Basic Linux', 'Photoshop (Basics)']
        }
        with open(SKILLS_FILE, 'w') as f:
            json.dump(default_skills, f, indent=2)

init_data_files()

# Helper functions
def load_certificates():
    with open(CERTIFICATES_FILE, 'r') as f:
        return json.load(f)

def save_certificates(data):
    with open(CERTIFICATES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_skills():
    with open(SKILLS_FILE, 'r') as f:
        return json.load(f)

def save_skills(data):
    with open(SKILLS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login to access admin panel', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    projects_data = [
        {
            'title': 'Automatic Timetable Generator',
            'status': 'Completed',
            'tech': ['PHP', 'MySQL', 'HTML', 'CSS'],
            'description': 'Built an automated timetable generation system to avoid teacher and classroom clashes',
            'features': [
                'Enabled easy schedule updates and reduced manual effort for academic planning'
            ]
        },
        {
            'title': 'AI Chatbot',
            'status': 'Ongoing',
            'tech': ['Python', 'Flask', 'NLP'],
            'description': 'Developing a domain-based chatbot to answer user queries using NLP techniques',
            'features': [
                'Implementing intent recognition for interactive communication generation'
            ]
        }
    ]
    return render_template('projects.html', projects=projects_data)

@app.route('/skills')
def skills():
    skills_data = load_skills()
    return render_template('skills.html', skills=skills_data)

@app.route('/education')
def education():
    education_data = [
        {
            'degree': 'Bachelor of Computer Applications',
            'period': '2022-2026',
            'institution': 'Bharata Mata College of Commerce & Arts, Choondy, Aluva'
        },
        {
            'degree': 'Higher Secondary Education — Computer Science',
            'period': '2021-2023',
            'institution': 'Christava Mahilalayam Public School'
        }
    ]
    certifications = [
        'Web Development (Elewayte)',
        'Cyber Security Add-on Certification (Tech By Heart)',
        'Attended AI & ML Orientation — Technovalley'
    ]
    leadership = [
        'NSS Volunteer — Active participation in social initiatives',
        'Internship at Talrop (2025 – Ongoing)'
    ]
    return render_template('education.html', 
                         education=education_data, 
                         certifications=certifications,
                         leadership=leadership)

@app.route('/certificates')
def certificates():
    certificates_data = load_certificates()
    return render_template('certificates.html', certificates=certificates_data)

@app.route('/contact')
def contact():
    contact_info = {
        'phone': '9744360607',
        'email': 'vinayaksunilkhosh@gmail.com',
        'github': 'https://github.com/Vinayak-S-Khosh',
        'linkedin': 'https://www.linkedin.com/in/vinayak-sunil-khosh-2005',
        'location': 'Ernakulam, Kerala'
    }
    return render_template('contact.html', contact=contact_info)

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    certificates = load_certificates()
    skills = load_skills()
    return render_template('admin_dashboard.html', certificates=certificates, skills=skills)

# Certificate Management
@app.route('/admin/certificates/add', methods=['POST'])
@admin_required
def add_certificate():
    certificates = load_certificates()
    new_cert = {
        'id': max([c.get('id', 0) for c in certificates], default=0) + 1,
        'name': request.form.get('name'),
        'issuer': request.form.get('issuer')
    }
    certificates.append(new_cert)
    save_certificates(certificates)
    flash('Certificate added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certificates/delete/<int:cert_id>', methods=['POST'])
@admin_required
def delete_certificate(cert_id):
    certificates = load_certificates()
    certificates = [c for c in certificates if c.get('id') != cert_id]
    save_certificates(certificates)
    flash('Certificate deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certificates/edit/<int:cert_id>', methods=['POST'])
@admin_required
def edit_certificate(cert_id):
    certificates = load_certificates()
    for cert in certificates:
        if cert.get('id') == cert_id:
            cert['name'] = request.form.get('name')
            cert['issuer'] = request.form.get('issuer')
            break
    save_certificates(certificates)
    flash('Certificate updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Skills Management
@app.route('/admin/skills/add', methods=['POST'])
@admin_required
def add_skill():
    skills = load_skills()
    category = request.form.get('category')
    skill_name = request.form.get('skill_name')
    
    if category in skills:
        if skill_name not in skills[category]:
            skills[category].append(skill_name)
            save_skills(skills)
            flash('Skill added successfully!', 'success')
        else:
            flash('Skill already exists in this category', 'warning')
    else:
        flash('Invalid category', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/skills/delete', methods=['POST'])
@admin_required
def delete_skill():
    skills = load_skills()
    category = request.form.get('category')
    skill_name = request.form.get('skill_name')
    
    if category in skills and skill_name in skills[category]:
        skills[category].remove(skill_name)
        save_skills(skills)
        flash('Skill deleted successfully!', 'success')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
