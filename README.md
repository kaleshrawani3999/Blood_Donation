# Blood_Donation
# 🩸 Blood Donation Management System

## 📌 Project Overview

The **Blood Donation Management System** is a web-based application designed to connect blood donors with recipients in need. It helps manage donor records, blood requests, camps, and provides real-time insights through dashboards.

---

## 🚀 Features

### 👤 Donor Management

* Register as a blood donor
* Store personal details (name, blood group, location, contact)
* Search donors by blood group and location

### 🏥 Blood Request System

* Request blood in emergency situations
* Filter donors based on requirement
* Send email alerts to matching donors

### 📅 Camp Management

* Add and manage blood donation camps
* View available camps

### 🔐 Admin Panel

* Secure admin login
* View donors and requests
* Manage system data

### 🤖 AI Chatbot

* Integrated AI assistant for answering blood donation queries

### 📊 Dashboard Visualization

* Data visualization using **Power BI**
* Insights like:

  * Blood group distribution
  * Total donors vs requests
  * Priority-based requests

---

## 🛠️ Technologies Used

### 💻 Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

### ⚙️ Backend

* Python (Flask Framework)

### 🗄️ Database

* MySQL

### 📊 Data Visualization

* Power BI

### 📧 Email Service

* SMTP (Gmail)

### 🤖 AI Integration

* OpenAI API

---

## 📂 Project Structure

```
project/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── register.html
│   ├── search.html
│   ├── admin_dashboard.html
│   └── about.html
│   ├── admin.html
│   ├── camps.html
│   ├── matche_donors.html
│   ├── add_camps.html
├── static/
│   ├── css/
│   ├── js/
│
└── database/
    └── blood_donation.sql
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/blood-donation-system.git
cd blood-donation-system
```

### 2️⃣ Install Dependencies

```
pip install flask mysql-connector-python openai
```

### 3️⃣ Setup MySQL Database

* Create database:

```
CREATE DATABASE blood_donation;
```

* Import SQL file

### 4️⃣ Configure Database in app.py

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="blood_donation"
)
```

### 5️⃣ Run the Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 📊 Power BI Dashboard

The system integrates with **Power BI** to visualize:

* Blood group availability
* Donor distribution
* Emergency request trends

---

## 🌟 Future Enhancements

* OTP-based authentication.
* SMS notifications

---

## 👩‍💻 Author

Shrawani Kale
---

## ❤️ Conclusion

This system helps save lives by connecting donors and recipients efficiently while providing real-time insights using modern technologies.

---
