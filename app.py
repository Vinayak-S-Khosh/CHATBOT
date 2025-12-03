from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, Response, send_from_directory
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from datetime import datetime, timedelta
import secrets
import sqlite3
import os
import csv
import io
import re
import sys

# Add PORTFOLIO directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PORTFOLIO'))

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = secrets.token_hex(16)  # For session management

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the Kalapuraparambil Automobiles intents
with open('kalapuraparambil_intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# Load the trained model
FILE = "kalapuraparambil_data.pth"
data = torch.load(FILE, map_location=torch.device('cpu'))

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Kalapuraparambil Auto Bot"

# Quick reply suggestions based on intent
QUICK_REPLIES = {
    'greeting': ['What services do you offer?', 'Tell me about caravans', 'Contact information'],
    'company_info': ['What are your services?', 'Why choose you?', 'View portfolio'],
    'services': ['Tell me about caravans', 'Force Urbania modification', 'Luxury interiors'],
    'caravan': ['How much does it cost?', 'How long does it take?', 'Book consultation'],
    'force_traveller': ['Show me examples', 'Get a quote', 'What features included?'],
    'force_urbania': ['Pricing details', 'Timeline', 'See past projects'],
    'contact': ['Book a consultation', 'Visit workshop', 'Get directions'],
    'default': ['Our services', 'Contact us', 'Why choose Kalapuraparambil?']
}

# Confidence thresholds
HIGH_CONFIDENCE = 0.85
MEDIUM_CONFIDENCE = 0.75
LOW_CONFIDENCE = 0.50

# Database setup
DATABASE = 'inquiries.db'

# Gallery images organized by category
GALLERY_IMAGES = {
    'urbania': [
        'images/urbania/IMG-20241119-WA0004.jpg',
        'images/urbania/IMG-20241119-WA0008.jpg',
        'images/urbania/IMG-20250627-WA0039.jpg',
        'images/urbania/IMG-20250719-WA0024.jpg',
        'images/urbania/WhatsApp Image 2025-06-17 at 14.43.59_54626bc7.jpg',
        'images/urbania/WhatsApp Image 2025-08-06 at 16.12.31_99582b16 - Copy.jpg'
    ],
    'caravan': [
        'images/caravan/IMG-20240405-WA0007.jpg',
        'images/caravan/IMG-20240405-WA0008.jpg',
        'images/caravan/PIC_8489.JPG',
        'images/caravan/WhatsApp Image 2022-06-15 at 2.44.58 PM (4).jpeg',
        'images/caravan/WhatsApp Image 2022-06-15 at 2.44.58 PM.jpeg',
        'images/caravan/WhatsApp Image 2022-06-15 at 2.44.59 PM (1).jpeg'
    ],
    'traveller': [
        'images/traveller/IMG-20240405-WA0003.jpg',
        'images/traveller/IMG-20240405-WA0004.jpg',
        'images/traveller/IMG-20240405-WA0005.jpg',
        'images/traveller/IMG-20240405-WA0006.jpg',
        'images/traveller/IMG-20240405-WA0009.jpg',
        'images/traveller/IMG-20240405-WA0010.jpg'
    ],
    'icu': [
        'images/icu/1 - Copy.JPG',
        'images/icu/15.jpg',
        'images/icu/20140826_132556.jpg',
        'images/icu/20140826_132616.jpg',
        'images/icu/WhatsApp Image 2022-05-23 at 6.24.11 PM.jpeg',
        'images/icu/WhatsApp Image 2022-05-23 at 6.24.12 PM (1).jpeg'
    ],
    'interior': [
        'images/interior/10 - Copy - Copy.jpg',
        'images/interior/12.jpg',
        'images/interior/632A0129.JPG',
        'images/interior/632A0132.JPG',
        'images/interior/DSC_0053.JPG',
        'images/interior/DSC_0347.JPG'
    ],
    'campaign': [
        'images/campaign/DSC_0344 - Copy.JPG',
        'images/campaign/DSC_0349.JPG'
    ]
}

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with inquiries table"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            service TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'new',
            priority TEXT DEFAULT 'medium',
            tags TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            follow_up_date DATE,
            assigned_to TEXT
        )
    ''')
    
    # Create admin users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create default admin if doesn't exist
    try:
        conn.execute("INSERT INTO admin_users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Admin already exists
    
    conn.close()

# Initialize database when app starts
init_db()

# Validation functions
def validate_phone(phone):
    """Validate Indian phone number"""
    # Remove spaces and special characters
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's a valid Indian number (10 digits or +91 followed by 10 digits)
    pattern = r'^(\+91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone_clean))

def validate_email(email):
    """Validate email format"""
    if not email or email == 'Not provided':
        return True  # Email is optional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_name(name):
    """Validate name - only letters and spaces, 2-50 characters"""
    if not name or len(name) < 2 or len(name) > 50:
        return False
    # Allow letters, spaces, dots, and common name characters
    pattern = r'^[a-zA-Z\s\.\-]+$'
    return bool(re.match(pattern, name))

def format_response(response, tag):
    """Format responses for better readability"""
    
    # Add structured formatting for certain intents
    if tag == 'services':
        if 'offer:' in response.lower() or '1)' in response:
            # Already formatted, return as is
            return response
        # Add formatting if needed
        response = response.replace('1)', '\n1)')
        response = response.replace('2)', '\n2)')
        response = response.replace('3)', '\n3)')
        response = response.replace('4)', '\n4)')
        response = response.replace('5)', '\n5)')
        response = response.replace('6)', '\n6)')
    
    elif tag in ['contact', 'location', 'working_hours']:
        # Add visual separators for contact info
        response = response.replace('Phone:', '\n\n📞 **Phone:**')
        response = response.replace('Email:', '\n📧 **Email:**')
        response = response.replace('Address:', '\n📍 **Address:**')
        response = response.replace('Hours:', '\n⏰ **Hours:**')
        
        # Add Google Maps directions link for location requests
        if tag == 'location':
            # Add a Google Maps directions link
            response += "\n\n🧭 **Get Directions:** [Click here for Google Maps directions](https://www.google.com/maps/dir/?api=1&destination=Kalapuraparambil+Automobiles,+Manakkappady,+Karumalloor+P+O,+North+Paravur,+Ernakulam,+Kerala+683511)"
    
    elif tag == 'why_choose':
        # Format list items
        response = response.replace('1)', '\n\n✓ ')
        response = response.replace('2)', '\n✓ ')
        response = response.replace('3)', '\n✓ ')
        response = response.replace('4)', '\n✓ ')
        response = response.replace('5)', '\n✓ ')
        response = response.replace('6)', '\n✓ ')
    
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html')

# Portfolio routes - serve as a sub-app with proper template rendering
PORTFOLIO_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'PORTFOLIO', 'templates')
PORTFOLIO_STATIC_DIR = os.path.join(os.path.dirname(__file__), 'PORTFOLIO', 'static')

@app.route('/portfolio')
@app.route('/portfolio/')
def portfolio_home():
    """Serve portfolio homepage with proper template rendering"""
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(PORTFOLIO_TEMPLATE_DIR))
    template = env.get_template('index.html')
    # Create a simple context with url_for functions and mocked Flask functions
    context = {
        'url_for': lambda endpoint, **kwargs: f"/portfolio/{endpoint.replace('_', '-')}" if endpoint != 'static' else f"/portfolio-static/{kwargs.get('filename', '')}",
        'request': type('Request', (), {'endpoint': 'home'})(),
        'get_flashed_messages': lambda with_categories=False: []  # Mock flash messages
    }
    return template.render(**context)

@app.route('/portfolio/<page>', methods=['GET', 'POST'])
def portfolio_pages(page):
    """Serve portfolio pages"""
    from jinja2 import Environment, FileSystemLoader
    import json as pjson
    
    env = Environment(loader=FileSystemLoader(PORTFOLIO_TEMPLATE_DIR))
    
    # Map URL-friendly names to template names
    page_map = {
        'about': 'about.html',
        'projects': 'projects.html',
        'skills': 'skills.html',
        'education': 'education.html',
        'certificates': 'certificates.html',
        'contact': 'contact.html',
        'admin-login': 'admin_login.html',
        'admin': 'admin_dashboard.html',
        'home': 'index.html'  # Add home mapping
    }
    
    template_file = page_map.get(page, f"{page}.html")
    try:
        template = env.get_template(template_file)
        
        # Base context with get_flashed_messages mock
        context = {
            'url_for': lambda endpoint, **kwargs: f"/portfolio/{endpoint.replace('_', '-')}" if endpoint != 'static' else f"/portfolio-static/{kwargs.get('filename', '')}",
            'request': type('Request', (), {'endpoint': page.replace('-', '_')})(),
            'get_flashed_messages': lambda with_categories=False: []  # Will be updated if there are errors
        }
        
        # Handle admin login
        if page == 'admin-login' and request.method == 'POST':
            password = request.form.get('password')
            if password == 'admin123':
                session['portfolio_admin'] = True
                return redirect('/portfolio/admin')
            else:
                # Add error message
                context['get_flashed_messages'] = lambda with_categories=False: [('error', 'Invalid password. Please try again.')] if with_categories else ['Invalid password. Please try again.']
        
        # Add page-specific data
        if page == 'projects':
            context['projects'] = [
                {
                    'title': 'Automatic Timetable Generator',
                    'status': 'Completed',
                    'tech': ['PHP', 'MySQL', 'HTML', 'CSS'],
                    'description': 'Built an automated timetable generation system to avoid teacher and classroom clashes',
                    'features': ['Enabled easy schedule updates and reduced manual effort for academic planning']
                },
                {
                    'title': 'AI Chatbot',
                    'status': 'Ongoing',
                    'tech': ['Python', 'Flask', 'NLP'],
                    'description': 'Developing a domain-based chatbot to answer user queries using NLP techniques',
                    'features': ['Implementing intent recognition for interactive communication generation']
                }
            ]
        elif page == 'skills':
            # Load skills from portfolio data file if exists, otherwise use defaults
            skills_file = os.path.join(os.path.dirname(__file__), 'PORTFOLIO', 'data', 'skills.json')
            if os.path.exists(skills_file):
                with open(skills_file, 'r') as f:
                    context['skills'] = pjson.load(f)
            else:
                context['skills'] = {
                    'programming': ['Python', 'PHP'],
                    'database': ['MySQL'],
                    'web': ['HTML', 'CSS'],
                    'ai_ml': ['NLP (Basics)'],
                    'tools': ['Git', 'Canva'],
                    'other': ['APIs', 'Basic Linux', 'Photoshop (Basics)']
                }
        elif page == 'education':
            context['education'] = [
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
            context['certifications'] = [
                'Web Development (Elewayte)',
                'Cyber Security Add-on Certification (Tech By Heart)',
                'Attended AI & ML Orientation — Technovalley'
            ]
            context['leadership'] = [
                'NSS Volunteer — Active participation in social initiatives',
                'Internship at Talrop (2025 – Ongoing)'
            ]
        elif page == 'certificates':
            certs_file = os.path.join(os.path.dirname(__file__), 'PORTFOLIO', 'data', 'certificates.json')
            if os.path.exists(certs_file):
                with open(certs_file, 'r') as f:
                    context['certificates'] = pjson.load(f)
            else:
                context['certificates'] = [
                    {'id': 1, 'name': 'Web Development', 'issuer': 'Elewayte'},
                    {'id': 2, 'name': 'Cyber Security Add-on Certification', 'issuer': 'Tech By Heart'},
                    {'id': 3, 'name': 'AI & ML Orientation', 'issuer': 'Technovalley'}
                ]
        elif page == 'contact':
            context['contact'] = {
                'phone': '9744360607',
                'email': 'vinayaksunilkhosh@gmail.com',
                'github': 'https://github.com/Vinayak-S-Khosh',
                'linkedin': 'https://www.linkedin.com/in/vinayak-sunil-khosh-2005',
                'location': 'Ernakulam, Kerala'
            }
        elif page == 'admin':
            # Check if admin is logged in
            if not session.get('portfolio_admin'):
                return redirect('/portfolio/admin-login')
            # Load admin data
            context['certificates'] = [
                {'id': 1, 'name': 'Web Development', 'issuer': 'Elewayte'},
                {'id': 2, 'name': 'Cyber Security Add-on Certification', 'issuer': 'Tech By Heart'},
                {'id': 3, 'name': 'AI & ML Orientation', 'issuer': 'Technovalley'}
            ]
            context['skills'] = {
                'programming': ['Python', 'PHP'],
                'database': ['MySQL'],
                'web': ['HTML', 'CSS'],
                'ai_ml': ['NLP (Basics)'],
                'tools': ['Git', 'Canva'],
                'other': ['APIs', 'Basic Linux', 'Photoshop (Basics)']
            }
        
        return template.render(**context)
    except Exception as e:
        return f"Error loading page: {str(e)}", 404

@app.route('/portfolio-static/<path:filename>')
def portfolio_static_files(filename):
    """Serve portfolio static files"""
    return send_from_directory(PORTFOLIO_STATIC_DIR, filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve images from the images directory"""
    return send_file(os.path.join('images', filename))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({
            'response': 'Please enter a message.',
            'confidence': 0,
            'suggestions': QUICK_REPLIES['default']
        })
    
    # Initialize session conversation history
    if 'conversation' not in session:
        session['conversation'] = []
        session['failed_attempts'] = 0
        session['last_intent'] = None
    
    # Check if user is asking for images/photos/examples
    user_message_lower = user_message.lower()
    image_keywords = ['image', 'images', 'photo', 'photos', 'picture', 'pictures', 'show me', 'example', 'examples', 'see', 'look', 'view', 'gallery', 'portfolio']
    is_asking_for_images = any(keyword in user_message_lower for keyword in image_keywords)
    
    # Detect vehicle category from current message or last intent
    category_detected = None
    category_map = {
        'urbania': ['urbania'],
        'caravan': ['caravan', 'mobile home', 'home on wheels'],
        'traveller': ['traveller', 'tourist', 'tour'],
        'icu': ['icu', 'ambulance', 'medical', 'hospital'],
        'interior': ['interior', 'luxury', 'wood', 'fiber'],
        'campaign': ['campaign', 'election', 'political']
    }
    
    for category, keywords in category_map.items():
        if any(keyword in user_message_lower for keyword in keywords):
            category_detected = category
            break
    
    # If asking for images and category is detected or was recently discussed
    if is_asking_for_images:
        # Use detected category or fall back to last discussed intent
        if not category_detected and session.get('last_intent'):
            intent_to_category = {
                'force_urbania': 'urbania',
                'caravan': 'caravan',
                'force_traveller': 'traveller',
                'special_purpose': 'icu',
                'luxury_interior': 'interior'
            }
            category_detected = intent_to_category.get(session.get('last_intent'))
        
        if category_detected and category_detected in GALLERY_IMAGES:
            images = random.sample(GALLERY_IMAGES[category_detected], min(3, len(GALLERY_IMAGES[category_detected])))
            
            category_names = {
                'urbania': 'Force Urbania',
                'caravan': 'Custom Caravan',
                'traveller': 'Force Traveller',
                'icu': 'Mobile ICU',
                'interior': 'Luxury Interior',
                'campaign': 'Campaign Vehicle'
            }
            
            response = f"Here are some examples of our {category_names.get(category_detected, category_detected)} projects:\n\n"
            for idx, img in enumerate(images, 1):
                response += f"![Image {idx}](/{img})\n\n"
            
            response += f"\nView more in our [Gallery](/gallery?category={category_detected})!"
            
            return jsonify({
                'response': response,
                'confidence': 100,
                'intent': 'image_request',
                'images': images,
                'suggestions': ['View full gallery', 'Tell me more about ' + category_names.get(category_detected, category_detected), 'Contact for quote']
            })
    
    # Add user message to history
    session['conversation'].append({
        'role': 'user',
        'message': user_message,
        'timestamp': datetime.now().isoformat()
    })
    
    # Tokenize and predict
    sentence = tokenize(user_message)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    confidence = probs[0][predicted.item()].item()

    # Determine response based on confidence level
    if confidence > MEDIUM_CONFIDENCE:
        session['failed_attempts'] = 0
        session['last_intent'] = tag  # Store the intent for image requests
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                
                # Format response for better readability
                response = format_response(response, tag)
                
                # Add helpful context for certain intents
                if tag in ['contact', 'location', 'working_hours']:
                    response += "\n\n💡 Tip: You can also click the chat bubble to ask more questions!"
                
                # Add image suggestion for vehicle-related intents
                if tag in ['force_urbania', 'caravan', 'force_traveller', 'special_purpose', 'luxury_interior']:
                    response += "\n\n📸 Want to see examples? Just ask 'show me images' or 'show photos'!"
                
                # Get relevant suggestions
                suggestions = QUICK_REPLIES.get(tag, QUICK_REPLIES['default'])
                
                # Add to conversation history
                session['conversation'].append({
                    'role': 'bot',
                    'message': response,
                    'confidence': confidence,
                    'intent': tag,
                    'timestamp': datetime.now().isoformat()
                })
                session.modified = True
                
                return jsonify({
                    'response': response,
                    'confidence': round(confidence * 100, 1),
                    'intent': tag,
                    'suggestions': suggestions
                })
    
    elif confidence > LOW_CONFIDENCE:
        # Medium confidence - ask for clarification
        session['failed_attempts'] += 1
        response = f"I think you're asking about {tag.replace('_', ' ')}. Could you please provide more details or rephrase your question?"
        suggestions = QUICK_REPLIES.get(tag, QUICK_REPLIES['default'])
        
        return jsonify({
            'response': response,
            'confidence': round(confidence * 100, 1),
            'suggestions': suggestions,
            'needsClarification': True
        })
    
    else:
        # Low confidence - provide help
        session['failed_attempts'] = session.get('failed_attempts', 0) + 1
        
        if session['failed_attempts'] >= 3:
            response = """I'm having trouble understanding. Let me connect you with our team:
            
📞 Phone: +91 81481 45706, +91 9847297290
📧 Email: kalapuraparambil.auto@gmail.com
⏰ Hours: Mon-Sat, 9 AM - 6 PM

Or try asking about:"""
            session['failed_attempts'] = 0
        else:
            response = "I'm not quite sure about that. Could you rephrase or try one of these questions?"
        
        suggestions = [
            'What services do you offer?',
            'Tell me about custom caravans',
            'How do I contact you?',
            'Show me your portfolio'
        ]
        
        return jsonify({
            'response': response,
            'confidence': round(confidence * 100, 1),
            'suggestions': suggestions,
            'lowConfidence': True
        })

@app.route('/reset-session', methods=['POST'])
def reset_session():
    """Clear conversation history"""
    session.clear()
    return jsonify({'status': 'success', 'message': 'Session reset'})

@app.route('/conversation-history', methods=['GET'])
def get_conversation_history():
    """Get conversation history for analytics"""
    return jsonify({
        'conversation': session.get('conversation', []),
        'messageCount': len(session.get('conversation', []))
    })

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions with validation and save to database"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip() or 'Not provided'
        service = data.get('service', '')
        message = data.get('message', '').strip()
        
        # Validate name
        if not validate_name(name):
            return jsonify({
                'status': 'error',
                'message': 'Invalid name. Please use only letters (2-50 characters).'
            }), 400
        
        # Validate phone
        if not validate_phone(phone):
            return jsonify({
                'status': 'error',
                'message': 'Invalid phone number. Please enter a valid Indian mobile number (10 digits).'
            }), 400
        
        # Validate email
        if not validate_email(email):
            return jsonify({
                'status': 'error',
                'message': 'Invalid email address. Please enter a valid email.'
            }), 400
        
        # Validate message
        if not message or len(message) < 10:
            return jsonify({
                'status': 'error',
                'message': 'Please provide a detailed message (at least 10 characters).'
            }), 400
        
        # Save to database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO inquiries (name, phone, email, service, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, email, service, message))
        conn.commit()
        conn.close()
        
        # Log to console
        inquiry_log = f"""
        ✅ New Inquiry Saved to Database:
        Name: {name}
        Phone: {phone}
        Email: {email}
        Service: {service}
        Message: {message}
        Timestamp: {datetime.now()}
        """
        print(inquiry_log)
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for your inquiry. We will contact you soon!'
        })
    except Exception as e:
        print(f"Error saving inquiry: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Something went wrong. Please try again or call us directly.'
        }), 500

@app.route('/admin/inquiries')
def view_inquiries():
    """Admin page to view all inquiries with filtering and search"""
    # Simple password check (not logged in via session)
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    # Get filter parameters
    search = request.args.get('search', '')
    status_filter = request.args.get('status', 'all')
    service_filter = request.args.get('service', 'all')
    priority_filter = request.args.get('priority', 'all')
    date_filter = request.args.get('date', 'all')
    
    # Build query
    query = 'SELECT * FROM inquiries WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (name LIKE ? OR phone LIKE ? OR email LIKE ? OR message LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param, search_param])
    
    if status_filter != 'all':
        query += ' AND status = ?'
        params.append(status_filter)
    
    if service_filter != 'all':
        query += ' AND service = ?'
        params.append(service_filter)
    
    if priority_filter != 'all':
        query += ' AND priority = ?'
        params.append(priority_filter)
    
    if date_filter != 'all':
        if date_filter == 'today':
            query += ' AND DATE(timestamp) = DATE("now")'
        elif date_filter == 'week':
            query += ' AND DATE(timestamp) >= DATE("now", "-7 days")'
        elif date_filter == 'month':
            query += ' AND DATE(timestamp) >= DATE("now", "-30 days")'
    
    query += ' ORDER BY timestamp DESC'
    
    inquiries = conn.execute(query, params).fetchall()
    
    # Get all unique services for filter dropdown
    services = conn.execute('SELECT DISTINCT service FROM inquiries').fetchall()
    
    conn.close()
    
    return render_template('admin_inquiries.html', 
                         inquiries=inquiries, 
                         services=services,
                         filters={
                             'search': search,
                             'status': status_filter,
                             'service': service_filter,
                             'priority': priority_filter,
                             'date': date_filter
                         })

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Simple admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM admin_users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('view_inquiries'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/mark-read/<int:inquiry_id>', methods=['POST'])
def mark_inquiry_read(inquiry_id):
    """Mark inquiry as read"""
    conn = get_db_connection()
    conn.execute('UPDATE inquiries SET status = ? WHERE id = ?', ('read', inquiry_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/admin/update-priority/<int:inquiry_id>', methods=['POST'])
def update_priority(inquiry_id):
    """Update inquiry priority"""
    data = request.json
    priority = data.get('priority', 'medium')
    
    conn = get_db_connection()
    conn.execute('UPDATE inquiries SET priority = ? WHERE id = ?', (priority, inquiry_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/admin/add-note/<int:inquiry_id>', methods=['POST'])
def add_note(inquiry_id):
    """Add note to inquiry"""
    data = request.json
    note = data.get('note', '')
    
    conn = get_db_connection()
    # Append to existing notes
    inquiry = conn.execute('SELECT notes FROM inquiries WHERE id = ?', (inquiry_id,)).fetchone()
    existing_notes = inquiry['notes'] if inquiry['notes'] else ''
    new_notes = f"{existing_notes}\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}" if existing_notes else f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}"
    
    conn.execute('UPDATE inquiries SET notes = ? WHERE id = ?', (new_notes, inquiry_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'notes': new_notes})

@app.route('/admin/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    """Delete inquiry"""
    conn = get_db_connection()
    conn.execute('DELETE FROM inquiries WHERE id = ?', (inquiry_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/admin/bulk-delete', methods=['POST'])
def bulk_delete():
    """Delete multiple inquiries"""
    data = request.json
    ids = data.get('ids', [])
    
    if ids:
        conn = get_db_connection()
        placeholders = ','.join('?' * len(ids))
        conn.execute(f'DELETE FROM inquiries WHERE id IN ({placeholders})', ids)
        conn.commit()
        conn.close()
    
    return jsonify({'status': 'success', 'deleted': len(ids)})

@app.route('/admin/export-csv')
def export_csv():
    """Export inquiries as CSV"""
    conn = get_db_connection()
    inquiries = conn.execute('SELECT * FROM inquiries ORDER BY timestamp DESC').fetchall()
    conn.close()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Service', 'Message', 'Status', 'Priority', 'Tags', 'Timestamp'])
    
    # Write data
    for inquiry in inquiries:
        writer.writerow([
            inquiry['id'],
            inquiry['name'],
            inquiry['phone'],
            inquiry['email'],
            inquiry['service'],
            inquiry['message'],
            inquiry['status'],
            inquiry['priority'],
            inquiry['tags'],
            inquiry['timestamp']
        ])
    
    # Prepare response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'inquiries_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/admin/update-status/<int:inquiry_id>', methods=['POST'])
def update_status(inquiry_id):
    """Update inquiry status"""
    data = request.json
    status = data.get('status', 'new')
    
    conn = get_db_connection()
    conn.execute('UPDATE inquiries SET status = ? WHERE id = ?', (status, inquiry_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/admin/add-tag/<int:inquiry_id>', methods=['POST'])
def add_tag(inquiry_id):
    """Add tag to inquiry"""
    data = request.json
    tag = data.get('tag', '')
    
    conn = get_db_connection()
    inquiry = conn.execute('SELECT tags FROM inquiries WHERE id = ?', (inquiry_id,)).fetchone()
    existing_tags = inquiry['tags'] if inquiry['tags'] else ''
    tags_list = [t.strip() for t in existing_tags.split(',') if t.strip()]
    
    if tag and tag not in tags_list:
        tags_list.append(tag)
    
    new_tags = ', '.join(tags_list)
    conn.execute('UPDATE inquiries SET tags = ? WHERE id = ?', (new_tags, inquiry_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'tags': new_tags})

@app.route('/admin/analytics-data')
def get_analytics_data():
    """Get analytics data for charts"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    period = request.args.get('period', 'weekly')  # weekly, monthly, yearly
    
    conn = get_db_connection()
    
    # Determine date range based on period
    if period == 'weekly':
        date_condition = 'DATE(timestamp) >= DATE("now", "-7 days")'
    elif period == 'monthly':
        date_condition = 'DATE(timestamp) >= DATE("now", "-30 days")'
    elif period == 'yearly':
        date_condition = 'DATE(timestamp) >= DATE("now", "-365 days")'
    else:
        date_condition = '1=1'  # All time
    
    # Get service-wise inquiry count
    query = f'''
        SELECT service, COUNT(*) as count 
        FROM inquiries 
        WHERE {date_condition}
        GROUP BY service
        ORDER BY count DESC
    '''
    
    results = conn.execute(query).fetchall()
    conn.close()
    
    # Format data for chart
    services = [row['service'] for row in results]
    counts = [row['count'] for row in results]
    
    return jsonify({
        'services': services,
        'counts': counts,
        'period': period
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
