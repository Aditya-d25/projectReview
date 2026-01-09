# 📚 ProjectReview - Academic Project Management System

A comprehensive Flask-based web application designed to streamline the evaluation and management of academic projects through multiple review stages. Built for educational institutions to manage final year engineering projects efficiently.

## 🌟 Features

### 👥 User Management
- **Role-based Access Control** (Admin & User roles)
- **Email OTP Verification** for registration and password recovery
- **Secure Authentication** with bcrypt password hashing
- **Session Management** with Flask sessions

### 📊 Project Data Management
- **Bulk Upload** via Excel files (.xlsx)
- **Automated Data Normalization** and validation
- **Comprehensive Project Tracking**:
  - Group information and project details
  - Student members with roll numbers
  - Guide and mentor assignment
  - Evaluator assignment (2 per group)
  - Division and domain tracking

### 📝 Multi-Stage Review System
- **6 Review Stages**: Mock (Review 0), Reviews 1-4, and Final Review
- **Individual Performance Evaluation** with customizable criteria
- **Group-level Questionnaires** (Yes/No/NA/NC responses)
- **Automated Mark Calculation** using MySQL generated columns
- **Attendance Tracking** for each review stage

### 📅 Scheduling & Panel Management
- **Visual Scheduling Interface** for review sessions
- **Panel Assignment** with track and location management
- **Evaluator Distribution** across groups
- **Real-time Schedule Updates**

### 📄 PDF Report Generation
- **Professional Report Templates** with college branding
- **Individual Student Reports** with detailed marks breakdown
- **Group Response Sheets** with questionnaire answers
- **Bulk PDF Generation** for entire batches
- **Digital Signature Support** for evaluators

### 📈 Analytics & Dashboard
- **Attendance Dashboard** with visual tracking
- **Performance Analytics** across review stages
- **Excel Export** functionality for all data
- **Real-time Progress Monitoring**

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **MySQL** - Relational database
- **bcrypt** - Password hashing
- **pandas** - Data processing
- **openpyxl** - Excel file handling
- **ReportLab** - PDF generation

### Frontend
- **HTML5/CSS3** - Responsive templates
- **Jinja2** - Template engine
- **JavaScript** - Interactive UI components

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ProjectReview.git
cd ProjectReview
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Login to MySQL
mysql -u root -p

# Create database and import schema
mysql -u root -p < final_Preview_Schema.sql
```

### 5. Environment Configuration
Create a `.env` file in the root directory:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=p_review

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_DEBUG=0
HOST=0.0.0.0
PORT=5000

# Email Configuration (for OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
```

### 6. Create Admin Files Directory
```bash
mkdir admin_files
```

### 7. Run the Application
```bash
python server.py
```

The application will be available at `http://localhost:5000`

## 📖 Usage Guide

### For Administrators

#### 1. Initial Setup
1. Access the login page at `/auth/login`
2. Register as admin (first user becomes admin)
3. Verify email using OTP

#### 2. Upload Project Data
1. Navigate to **Data Manager** (`/data-manager`)
2. Upload Excel file with project and student data
3. System automatically validates and imports data

#### 3. Schedule Reviews
1. Go to **Scheduler** (`/scheduler`)
2. Assign evaluators to project groups
3. Set panel assignments and locations
4. Export schedule as PDF

#### 4. Conduct Reviews
1. Navigate to specific review page (e.g., `/review1`)
2. Mark student attendance
3. Enter marks for each performance criterion
4. Fill group questionnaire responses
5. Save evaluation data

#### 5. Generate Reports
1. Go to **PDF Viewer** (`/pdf-viewer`)
2. Select review stage and groups
3. Generate individual or bulk PDFs
4. Download reports for distribution

### For Evaluators (Users)

1. **Login** with credentials
2. **View assigned groups** on dashboard
3. **Enter marks** during review sessions
4. **Mark attendance** for students
5. **View final sheets** and performance data

## 📁 Project Structure

```
ProjectReview/
│
├── backend/
│   ├── api.py                 # REST API endpoints
│   ├── auth.py                # Authentication & authorization
│   ├── data_manager.py        # Excel upload & data management
│   ├── db.py                  # Database connection utilities
│   ├── email_service.py       # Email OTP service
│   ├── pdf_generator.py       # PDF report generation
│   ├── scheduler.py           # Review scheduling logic
│   └── otp_storage.py         # OTP management
│
├── frontend/
│   ├── static/                # CSS, JS, images
│   └── templates/             # HTML templates
│       ├── login.html
│       ├── register.html
│       ├── review0.html - review4.html
│       ├── data-manager.html
│       ├── scheduler.html
│       ├── pdf_viewer.html
│       └── attendance-dashboard.html
│
├── admin_files/               # Uploaded Excel files storage
├── final_Preview_Schema.sql   # Database schema
├── requirements.txt           # Python dependencies
├── server.py                  # Main application entry point
└── README.md
```

## 🗄️ Database Schema

### Key Tables
- **projects** - Master project information
- **members** - Student details and attendance tracking
- **review0_marks to review4_marks** - Individual performance evaluations
- **review0_questions to review4_questions** - Question banks
- **review0_group_responses to review4_group_responses** - Group assessments
- **users** - Authentication and user management
- **panel_assignments** - Scheduling and panel information

## 🔐 Security Features

- **Password Hashing** with bcrypt
- **Session-based Authentication**
- **Role-based Access Control** with decorators
- **SQL Injection Prevention** using parameterized queries
- **Email Verification** via OTP
- **Secure Password Recovery**

## 📊 Review Stages & Marking Scheme

### Review 0 (Mock Review)
- Practice evaluation session
- Same structure as formal reviews

### Review 1 (25 Marks)
- Understanding background and topic (2)
- Project scope and objectives (2)
- Literature survey (5)
- Project planning (4)
- Student contribution (4)
- Presentation skills (4)
- Q&A session (4)

### Review 2 (33 Marks)
- System architecture & literature (0)
- Project design (9)
- Methodology & algorithms (9)
- Project planning (2)
- Implementation details (5)
- Presentation skills (4)
- Q&A session (4)

### Reviews 3 & 4
- Progressive implementation evaluation
- Similar criteria with increased implementation focus

## 🔧 Configuration

### Excel Upload Format
Your Excel file should contain the following columns:
- Group No.
- Roll No.
- Name of the group member
- Contact details
- Division
- Project Domain
- Project Title
- Name of Guide
- Name of Mentor
- Email of Mentor
- Contact Details of Mentor
- Name of Sponsor Company (if any)

### Email Configuration
For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use this password in `.env` file

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check MySQL service status
# Windows: services.msc
# Linux: sudo systemctl status mysql
```

### Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Port Already in Use
```bash
# Change port in .env file
PORT=8080
```



## 👨‍💻 Author
GitHub - [https://github.com/Aditya-d25]
