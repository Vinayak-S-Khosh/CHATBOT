# Admin Panel Guide 🔐

## Overview
Your portfolio now has a **password-protected admin panel** where you can manage certificates and skills without editing code!

---

## 🔑 Accessing the Admin Panel

### Method 1: Direct URL
Visit: `http://localhost:5000/admin/login`

### Method 2: Hidden Footer Link
- Scroll to the bottom of any page
- Look for a small key icon (🔑) near the copyright text
- It's intentionally subtle so visitors won't notice it
- Click it to access admin login

---

## 🔐 Login Credentials

**Default Password:** `admin123`

**⚠️ IMPORTANT: Change the password before deploying!**

To change the password:
1. Open `app.py`
2. Find line 13: `app.config['ADMIN_PASSWORD'] = 'admin123'`
3. Change `'admin123'` to your strong password
4. Save the file
5. Restart the Flask server

---

## 📊 Admin Dashboard Features

### 1. **Certificates Management**
- ✅ View all certificates in a table
- ✅ Add new certificates
- ✅ Edit existing certificates
- ✅ Delete certificates
- ✅ Auto-incrementing IDs

### 2. **Skills Management**
- ✅ View skills organized by category
- ✅ Add skills to any category
- ✅ Delete skills
- ✅ 6 predefined categories:
  - Programming
  - Database
  - Web Development
  - AI/ML
  - Tools
  - Other

---

## 📝 How to Use

### Adding a Certificate

1. Login to admin panel
2. Click **"Add Certificate"** button
3. Fill in:
   - **Certificate Name**: e.g., "Python for Data Science"
   - **Issuer**: e.g., "Coursera"
4. Click **"Add Certificate"**
5. **Don't forget**: Add certificate image to `static/images/`
   - File name format: `cert_X.jpg` (where X is the certificate ID)

### Editing a Certificate

1. Find the certificate in the table
2. Click **"Edit"** button
3. Modify name or issuer
4. Click **"Save Changes"**

### Deleting a Certificate

1. Find the certificate in the table
2. Click **"Delete"** button
3. Confirm deletion

### Adding a Skill

1. Login to admin panel
2. Click **"Add Skill"** button
3. Select:
   - **Category**: Choose from dropdown
   - **Skill Name**: e.g., "React.js"
4. Click **"Add Skill"**

### Deleting a Skill

1. Find the skill under its category
2. Click the **X** icon next to the skill
3. Confirm deletion

---

## 📁 Data Storage

All changes are stored in **JSON files** in the `data/` folder:

- `data/certificates.json` - All certificates
- `data/skills.json` - All skills by category

**Format Example:**

`certificates.json`:
```json
[
  {
    "id": 1,
    "name": "Web Development",
    "issuer": "Elewayte"
  }
]
```

`skills.json`:
```json
{
  "programming": ["Python", "PHP"],
  "database": ["MySQL"]
}
```

---

## 🔒 Security Features

### 1. **Password Protection**
- Session-based authentication
- Must login to access any admin route
- Auto-redirect if not logged in

### 2. **Hidden Access**
- Admin link is subtle and hidden
- URL not advertised on the site
- Only you know where to find it

### 3. **Logout Function**
- **Logout** button in dashboard
- Clears admin session
- Redirects to homepage

---

## 🎯 Best Practices

### Certificate Images
After adding a certificate:
1. Note the certificate ID shown in the dashboard
2. Prepare your certificate image
3. Name it: `cert_[ID].jpg` (e.g., `cert_4.jpg`)
4. Place in: `static/images/`
5. Supported formats: `.jpg`, `.jpeg`, `.png`
6. Recommended size: 400x300px

### Security
1. **Change default password immediately**
2. Use a strong password (mix of letters, numbers, symbols)
3. Don't share the admin URL publicly
4. Logout when done managing content
5. Consider using environment variables for password in production

### Data Backup
1. Regularly backup `data/certificates.json`
2. Regularly backup `data/skills.json`
3. Keep backups before major changes

---

## 🚀 Production Deployment

### Environment Variable (Recommended)

Instead of hardcoding password, use environment variable:

**1. Update `app.py`:**
```python
import os
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')
```

**2. Set environment variable on server:**

**Linux/Mac:**
```bash
export ADMIN_PASSWORD='your_secure_password'
```

**Windows:**
```cmd
set ADMIN_PASSWORD=your_secure_password
```

**Heroku:**
```bash
heroku config:set ADMIN_PASSWORD=your_secure_password
```

**PythonAnywhere:**
- Go to Web tab
- Add environment variable in "Environment variables" section

---

## 📋 Admin Routes Reference

| URL | Method | Description | Auth Required |
|-----|--------|-------------|---------------|
| `/admin/login` | GET, POST | Admin login page | No |
| `/admin/logout` | GET | Logout admin | No |
| `/admin` | GET | Admin dashboard | Yes |
| `/admin/certificates/add` | POST | Add certificate | Yes |
| `/admin/certificates/edit/<id>` | POST | Edit certificate | Yes |
| `/admin/certificates/delete/<id>` | POST | Delete certificate | Yes |
| `/admin/skills/add` | POST | Add skill | Yes |
| `/admin/skills/delete` | POST | Delete skill | Yes |

---

## ⚡ Quick Actions

### Change Password
```python
# In app.py, line 13:
app.config['ADMIN_PASSWORD'] = 'YOUR_NEW_PASSWORD_HERE'
```

### Add New Skill Category
```python
# In data/skills.json, add:
{
  "programming": [...],
  "database": [...],
  "new_category": []  # ← Add this
}
```

### Reset All Data
Delete `data/` folder and restart server - it will recreate with defaults.

---

## 🐛 Troubleshooting

### Can't Login
- **Issue**: "Invalid password" error
- **Solution**: Check `app.py` line 13 for correct password

### Changes Not Showing
- **Issue**: Added certificate/skill but not visible
- **Solution**: 
  1. Check if you're logged in
  2. Refresh the main website
  3. Check `data/` folder for updated JSON files

### Lost Admin Password
- **Issue**: Forgot password
- **Solution**: 
  1. Open `app.py`
  2. Check line 13 for the password
  3. Or change it to a new one

### Data Files Missing
- **Issue**: `data/` folder empty
- **Solution**: Restart Flask server - it auto-creates files

---

## 💡 Tips

1. **Test First**: Add/edit/delete test items before production
2. **Backup**: Copy `data/` folder before bulk changes
3. **Images**: Prepare images before adding certificates
4. **Categories**: Keep skill categories organized and consistent
5. **Security**: Don't commit password to Git

---

## 📞 Admin Support

### Common Tasks

**Change password:**
```python
# app.py line 13
app.config['ADMIN_PASSWORD'] = 'new_password_here'
```

**Access admin:**
1. Go to: `http://localhost:5000/admin/login`
2. Enter password
3. Manage content

**Logout:**
Click "Logout" button in dashboard

---

## ✨ Features Summary

✅ **No code editing required** - Manage via web interface  
✅ **Password protected** - Only you can access  
✅ **Hidden from visitors** - Subtle footer link  
✅ **Instant updates** - Changes reflect immediately  
✅ **JSON storage** - Easy to backup and migrate  
✅ **User-friendly** - Clean, modern interface  
✅ **Mobile responsive** - Works on all devices  
✅ **Session-based** - Secure authentication  

---

**Your portfolio now has a professional content management system!** 🎉

**Admin URL**: `http://localhost:5000/admin/login`  
**Default Password**: `admin123` (change immediately!)

---

**Last Updated**: November 2024  
**Version**: 1.0
