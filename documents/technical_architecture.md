# Technical Architecture Documentation

## System Architecture Overview

### 1. Frontend Architecture
```
Frontend Layer
├── Templates
│   ├── Base Templates
│   │   ├── base.html
│   │   └── userbase.html
│   ├── Admin Templates
│   ├── Doctor Templates
│   └── User Templates
├── Static Files
│   ├── CSS
│   │   ├── style.css
│   │   └── custom.css
│   ├── JavaScript
│   │   ├── script.js
│   │   └── custom.js
│   └── Images
└── Media Files
    ├── Profile Pictures
    └── Prescriptions
```

### 2. Backend Architecture
```
Backend Layer
├── Django Framework
│   ├── URL Routing
│   ├── View Functions
│   ├── Models
│   └── Forms
├── Database Layer
│   └── MySQL Database
├── External Services
│   ├── Email Service (Gmail SMTP)
│   └── Payment Gateway (Stripe)
└── Authentication System
    └── Custom User Model
```

## Database Design

### Entity Relationship Diagram
```
CustomUser
    │
    ├── DoctorReg
    │       │
    │       └── Specialization
    │
    └── Appointment
            │
            └── OnlineConsultation
```

### Table Structures

#### CustomUser
```sql
CREATE TABLE dasapp_customuser (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128),
    last_login DATETIME,
    is_superuser BOOLEAN,
    username VARCHAR(150),
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN,
    is_active BOOLEAN,
    date_joined DATETIME,
    user_type VARCHAR(50)
);
```

#### DoctorReg
```sql
CREATE TABLE dasapp_doctorreg (
    id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT,
    specialization_id INT,
    address TEXT,
    mobile VARCHAR(11),
    status INT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (admin_id) REFERENCES dasapp_customuser(id),
    FOREIGN KEY (specialization_id) REFERENCES dasapp_specialization(id)
);
```

#### Appointment
```sql
CREATE TABLE dasapp_appointment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    appointmentnumber INT,
    fullname VARCHAR(250),
    mobilenumber VARCHAR(11),
    email VARCHAR(100),
    date_of_appointment VARCHAR(250),
    time_of_appointment VARCHAR(250),
    doctor_id_id INT,
    additional_msg TEXT,
    remark VARCHAR(250),
    status VARCHAR(200),
    prescription TEXT,
    recommendedtest TEXT,
    payment_status VARCHAR(20),
    stripe_payment_intent_id VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (doctor_id_id) REFERENCES dasapp_doctorreg(id)
);
```

## API Documentation

### Authentication Endpoints

#### Login
```http
POST /login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

#### Register
```http
POST /register/
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Appointment Endpoints

#### Create Appointment
```http
POST /appointment/
Content-Type: application/json

{
    "fullname": "John Doe",
    "email": "john@example.com",
    "mobilenumber": "1234567890",
    "date_of_appointment": "2024-05-10",
    "time_of_appointment": "14:30",
    "doctor_id": 1,
    "additional_msg": "Regular checkup"
}
```

#### View Appointments
```http
GET /view-appointment/
Authorization: Bearer <token>
```

## Security Implementation

### 1. Authentication
- Custom user model with role-based access
- Session-based authentication
- CSRF protection
- Password hashing

### 2. Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- Secure password storage

### 3. Payment Security
- Stripe integration
- PCI compliance
- Secure transaction handling
- Webhook verification

## Deployment Architecture

### Development Environment
```
Local Development
├── Django Development Server
├── MySQL Database
└── XAMPP Server
```

### Production Environment
```
Production Server
├── Web Server (Apache/Nginx)
├── Application Server (Gunicorn)
├── Database Server (MySQL)
└── Cache Server (Redis)
```

## Performance Optimization

### 1. Database Optimization
- Indexed fields
- Query optimization
- Connection pooling
- Caching strategies

### 2. Frontend Optimization
- Static file caching
- Image optimization
- Minified CSS/JS
- Lazy loading

### 3. Backend Optimization
- Query caching
- Database indexing
- Connection pooling
- Asynchronous tasks

## Monitoring and Logging

### 1. Application Logging
```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    logger.info("Function called")
    try:
        # Function logic
        pass
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
```

### 2. Error Tracking
- Exception handling
- Error logging
- Performance monitoring
- User activity tracking

## Backup and Recovery

### 1. Database Backup
```bash
# Backup command
mysqldump -u root -p doctorappointment > backup.sql

# Restore command
mysql -u root -p doctorappointment < backup.sql
```

### 2. File System Backup
- Regular backups
- Incremental backups
- Backup verification
- Recovery testing

## Development Workflow

### 1. Version Control
```
Git Workflow
├── Feature Branch
├── Development Branch
└── Production Branch
```

### 2. Testing Strategy
- Unit testing
- Integration testing
- End-to-end testing
- Performance testing

## Maintenance Procedures

### 1. Regular Maintenance
- Database optimization
- Log rotation
- Cache clearing
- Security updates

### 2. Emergency Procedures
- Backup restoration
- Error recovery
- Service restoration
- Incident response 