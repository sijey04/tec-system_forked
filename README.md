# TEC System - Testing and Evaluation Center Management System

A comprehensive web application for managing test center appointments, scheduling, and exam results. Built with Django REST Framework backend and Vue.js frontend.

## 📋 Features

- **User Management**: Registration and authentication for candidates and administrators
- **Appointment Scheduling**: Book and manage test appointments
- **Test Center Management**: Allocate test rooms and time slots
- **Status Tracking**: Monitor application status from submission to completion
- **Admin Dashboard**: Comprehensive overview of all appointments and statistics
- **Responsive UI**: Modern interface that works across devices

## 🛠️ Tech Stack

### Backend
- Django & Django REST Framework
- PostgreSQL database
- JWT Authentication

### Frontend
- Vue.js 3 with Composition API
- Tailwind CSS for styling
- Vite as build tool

## �� Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 14 or higher
- PostgreSQL or MySQL database (or SQLite for development)
- Git

### Installation

1. **Clone the repository**
   `ash
   git clone https://github.com/sijey04/tec-system_forked.git
   cd tec-system_forked
   `

2. **Set up the Backend**
   `ash
   # Navigate to backend directory
   cd backend
   
   # Create a virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # For Windows
   venv\Scripts\activate
   # For macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   pip install -r ../requirements.txt
   
   # Apply migrations
   python manage.py migrate
   
   # Create superuser (for admin access)
   python manage.py createsuperuser
   `

3. **Set up the Frontend**
   `ash
   # Navigate to frontend directory
   cd ../frontend
   
   # Install dependencies
   npm install
   `

### Running the Application

1. **Start the Backend Server**
   `ash
   # From the backend directory with activated virtual environment
   python manage.py runserver
   `
   The API will be available at http://localhost:8000/

2. **Start the Frontend Development Server**
   `ash
   # From the frontend directory
   npm run dev
   `
   The frontend will be available at http://localhost:5173/

3. **Using VS Code Tasks (Alternative)**
   
   This repository includes VS Code tasks for easier development:
   - Open the project in VS Code
   - Press Ctrl+Shift+P and select \
Tasks:
Run
Task\
   - Choose \Run
Django
Development
Server\

## 🗄️ Database Setup

The project includes a sample database file (	ecdb.sql) that you can import to get started with predefined data:

`ash
# For PostgreSQL
psql -U postgres -d your_database_name < tecdb.sql

# For MySQL
mysql -u root -p your_database_name < tecdb.sql
`

## 📑 API Documentation

API endpoints can be explored through the built-in Django REST Framework browsable API:
- Navigate to http://localhost:8000/api/ after starting the backend server

## 📱 Key User Workflows

### Student/Applicant
1. Register an account
2. Book an appointment by selecting program, date, and time slot
3. Submit required information and documentation
4. Check status and view appointment details
5. Receive test results after completion

### Administrator
1. View dashboard with key statistics
2. Process pending appointments
3. Assign test rooms and time slots
4. Update appointment status (waiting_for_submission, submitted, claimed, etc.)
5. Upload and manage test scores
6. Generate reports

## 🧪 Sample Data

The system includes sample data for testing:
- Test centers and rooms configured
- Sample programs and schools
- Example appointments at various stages
- Sample exam scores in CSV format

## 📈 Development Roadmap

- Email notifications for appointment status changes
- SMS notifications for reminders
- Report generation and exports
- Mobile application integration

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
