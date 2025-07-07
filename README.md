# 🍋 Little Lemon API – Meta Backend Developer Capstone

![Coursera](https://img.shields.io/badge/Coursera-0747a6?style=flat&logo=coursera&logoColor=white)
![Meta](https://img.shields.io/badge/Meta-0668E1?style=flat&logo=meta&logoColor=white)
![Django](https://img.shields.io/badge/Django-092e20?style=flat&logo=django&logoColor=white)

A Django REST API project built for the **Meta Back-End Developer Capstone Project** on [Coursera](https://www.coursera.org/).  
This project simulates the backend system for **Little Lemon**, a fictional restaurant.

---

## 📚 Project Purpose

This repository demonstrates:

- Django REST API development
- Token-based authentication
- MySQL database integration
- Booking and menu management
- Backend project structure following Django best practices

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/ongunakaycom/coursera-little-lemon-mysq.git
cd coursera-little-lemon-mysq
```

### 2. Create a .env file in the root folder
```
SECRET_KEY="your-secret-key"
DB_NAME="db"
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER="root"
DB_PASSWORD=""
```
###  3. Install dependencies and apply migrations
```
pipenv install
pipenv run python3 manage.py makemigrations
pipenv run python3 manage.py migrate
```

### 4. Run the development server
``` 
pipenv run python3 manage.py runserver
```

### 🔐 Authentication

- Uses Django REST Framework's authtoken
- Authentication required to book a table
- Only superusers can access full booking or menu control
- Login and token generation endpoints are defined in:
📁 authn/urls.py

### 🔍 API Endpoints
| Endpoint            | Description         | Auth Required |
| ------------------- | ------------------- | ------------- |
| `/restaurant/`      | Homepage (HTML)     | ❌ No          |
| `/restaurant/menu/` | GET/POST Menu Items | ✅ Superuser   |
| `/restaurant/book/` | GET/POST Bookings   | ✅ User        |

### 🧑‍💼 Roles & Permissions
- Anonymous Users: View homepage only
- Authenticated Users: Can create bookings
- Superusers: Can add/edit menu and view all bookings

### 🗂️ Project Structure
```
/
├── authn/              # Authentication endpoints
├── restaurant/         # Menu & booking logic
├── restaurant_api/     # API configuration
├── templates/          # HTML templates
├── static/             # Static files
├── manage.py
├── Pipfile / Pipfile.lock
├── .env                # Environment variables (ignored in Git)
├── requirements.txt
└── README.md
```

### 👨‍💻 About Me
I'm Ongun Akay, a Senior Full-Stack Developer with expertise across various technologies.

👀 I specialize in full-stack development with extensive experience in frontend and backend technologies.
🌱 Currently, I'm sharpening my skills in advanced concepts of web development.
💞️ I’m always open to exciting collaborations and projects that challenge my abilities.
📫 You can reach me at info@ongunakay.com.
