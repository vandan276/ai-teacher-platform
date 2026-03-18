# AI Teacher Upskilling Training Monitoring Platform

A centralized web platform to monitor large-scale teacher training programs.

## Features
- **Role-Based Access Control**: Admin, Employee, and Participant (Teacher) roles.
- **Admin**: Manage users, modules, assessments, and monitor district-wide progress.
- **Employee**: Monitor specific districts and track teacher progress.
- **Participant**: Access training modules, take MCQ assessments, and earn trophies.
- **Data Visualization**: Real-time charts for registration and completion tracking.

## Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Charts.js)
- **Database**: MySQL

## Setup Instructions

### 1. Database Setup
Create a MySQL database named `teacher_platform` and run the provided `schema.sql` to setup tables and initial data.
```bash
mysql -u your_username -p teacher_platform < schema.sql
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=teacher_platform
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
The app will be available at `http://localhost:5001`.

## Default Credentials
- **Admin**: `admin@example.com` / `admin123`

## Project Structure
- `app.py`: Main entry point.
- `routes/`: Blueprint definitions for each role.
- `templates/`: Jinja2 UI templates using Tailwind CSS.
- `utils/`: Custom decorators for security/RBAC.
- `schema.sql`: Database definition.
