# Doctor Appointment System Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Technology Stack](#technology-stack)
4. [Features](#features)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Installation Guide](#installation-guide)
8. [Configuration](#configuration)
9. [User Roles and Permissions](#user-roles-and-permissions)
10. [Email Integration](#email-integration)
11. [Payment Integration](#payment-integration)

## Project Overview
The Doctor Appointment System is a web-based application that facilitates the management of medical appointments between patients and doctors. The system provides features for appointment scheduling, online consultations, payment processing, and automated email notifications.

## Project Structure
```
docappsystem/
├── dasapp/                      # Main application directory
│   ├── migrations/             # Database migrations
│   ├── templates/              # HTML templates
│   │   ├── admin/             # Admin interface templates
│   │   ├── doc/               # Doctor interface templates
│   │   ├── emails/            # Email templates
│   │   └── user/              # User interface templates
│   ├── models.py              # Database models
│   ├── utils.py               # Utility functions
│   └── views.py               # View functions
├── docappsystem/              # Project configuration
│   ├── settings.py            # Project settings
│   ├── urls.py                # URL routing
│   └── wsgi.py               # WSGI configuration
├── static/                    # Static files
│   ├── assets/               # CSS, JS, and images
│   └── css/                  # Additional CSS files
├── templates/                 # Base templates
├── media/                     # User-uploaded files
└── documents/                 # Project documentation
```

## Technology Stack
- **Backend Framework**: Django 5.0.2
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Payment Gateway**: Stripe
- **Email Service**: Gmail SMTP
- **Web Server**: XAMPP

## Features

### 1. User Management
- User registration and authentication
- Role-based access control (Admin, Doctor, Patient)
- Profile management

### 2. Appointment Management
- Appointment scheduling
- Appointment status tracking
- Appointment history
- Online consultation scheduling

### 3. Doctor Features
- Doctor profile management
- Appointment management
- Patient records
- Online consultation management

### 4. Patient Features
- Appointment booking
- Appointment history
- Online consultation access
- Payment processing

### 5. Admin Features
- User management
- Doctor management
- System configuration
- Reports and analytics

## Database Schema

### CustomUser Model
- User authentication and authorization
- Role-based access control
- Profile information

### DoctorReg Model
- Doctor profile information
- Specialization
- Contact details

### Appointment Model
- Appointment details
- Patient information
- Doctor information
- Status tracking
- Payment information

### OnlineConsultation Model
- Meeting details
- Scheduling information
- Access credentials

## API Endpoints

### Authentication
- `/login/` - User login
- `/logout/` - User logout
- `/register/` - User registration

### Appointments
- `/appointment/` - Create appointment
- `/view-appointment/` - View appointments
- `/appointment-details/<id>/` - Appointment details

### Online Consultation
- `/schedule-consultation/<id>/` - Schedule online consultation
- `/join-meeting/<id>/` - Join online consultation

### Payment
- `/payment-success/` - Payment success handler
- `/stripe-webhook/` - Stripe webhook handler

## Installation Guide

1. **Prerequisites**
   - Python 3.8+
   - MySQL
   - XAMPP
   - Git

2. **Setup Steps**
   ```bash
   # Clone the repository
   git clone [repository-url]

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   # Install dependencies
   pip install -r requirements.txt

   # Configure database
   # Update settings.py with database credentials

   # Run migrations
   python manage.py migrate

   # Create superuser
   python manage.py createsuperuser

   # Run development server
   python manage.py runserver
   ```

## Configuration

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'doctorappointment',
        'USER': 'root',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '3307',
    }
}
```

### Email Configuration
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Stripe Configuration
```python
STRIPE_SECRET_KEY = 'your-stripe-secret-key'
```

## User Roles and Permissions

### Admin
- Full system access
- User management
- System configuration
- Reports and analytics

### Doctor
- Profile management
- Appointment management
- Patient records
- Online consultation management

### Patient
- Appointment booking
- Profile management
- Payment processing
- Online consultation access

## Email Integration
The system uses Gmail SMTP for sending automated emails:
- Appointment confirmations
- Online consultation details
- Payment confirmations
- Status updates

## Payment Integration
The system integrates with Stripe for payment processing:
- Secure payment handling
- Multiple payment methods
- Automated payment confirmation
- Webhook integration for payment status updates

## Security Considerations
1. **Data Protection**
   - Encrypted data transmission
   - Secure password storage
   - Session management

2. **Access Control**
   - Role-based permissions
   - Authentication requirements
   - Secure API endpoints

3. **Payment Security**
   - PCI compliance
   - Secure payment processing
   - Transaction encryption

## Maintenance and Support
1. **Regular Updates**
   - Security patches
   - Feature updates
   - Bug fixes

2. **Backup Procedures**
   - Database backups
   - File system backups
   - Recovery procedures

3. **Monitoring**
   - System performance
   - Error logging
   - User activity

## Future Enhancements
1. **Planned Features**
   - Mobile application
   - Video consultation
   - Prescription management
   - Medical records system

2. **Integration Possibilities**
   - Pharmacy integration
   - Insurance provider integration
   - Laboratory integration

## Troubleshooting Guide
1. **Common Issues**
   - Email configuration
   - Payment processing
   - Database connection
   - File uploads

2. **Solutions**
   - Configuration checks
   - Log analysis
   - Database maintenance
   - Cache clearing 