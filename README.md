# 📦 Dockerized Flask + PostgreSQL Quotes App

A fully containerized backend web application built with **Python (Flask)**, **PostgreSQL**, and **Docker Compose**.
This project demonstrates **multi-container orchestration**, **persistent storage**, and **real-world backend architecture**.

---

## 🚀 Features

* 🐍 Flask web application
* 🐘 PostgreSQL database
* 🐳 Docker & Docker Compose
* 🔗 Multi-container communication
* 💾 Persistent database storage via Docker volumes
* 📄 Add and display quotes
* ⚡ Fully reproducible development environment

---

## 🏗 Architecture

```
Browser
   ↓
Flask Web App (Container)
   ↓
PostgreSQL Database (Container)
```

---

## 📁 Project Structure

```
quotes-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   ├── index.html
│   └── add.html
└── README.md
```

---

## 🐳 Docker Services

| Service | Description               |
| ------- | ------------------------- |
| web     | Flask backend application |
| db      | PostgreSQL database       |
| volume  | Persistent data storage   |

---

## ⚙️ Prerequisites

* Docker Desktop
* Docker Compose
* Git (optional)

---

## ▶️ How To Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/quotes-app.git
cd quotes-app
```

---

### 2️⃣ Build & Start Containers

```bash
docker compose up --build
```

---

### 3️⃣ Open in Browser

```
http://localhost:5000
```

---

## 🧪 Testing The Application

1. Open:

   ```
   http://localhost:5000
   ```
2. Click **Add a new quote**
3. Submit a quote
4. The quote will be stored in PostgreSQL and displayed on the homepage

---

## 💾 Database Persistence

This project uses **Docker volumes** to persist PostgreSQL data.
Data remains stored even after stopping the containers.

---

## 🛠 Tech Stack

* Python 3.12
* Flask
* PostgreSQL 16
* Docker
* Docker Compose

---

## 📌 Learning Outcomes

* Docker image creation
* Multi-container orchestration
* Flask + PostgreSQL integration
* Environment isolation
* Container debugging

---

## 🚀 Future Improvements

* Add NGINX reverse proxy
* Add Redis caching
* Implement authentication
* Add REST API endpoints
* Deploy to cloud (AWS / Azure / GCP)

---

## 👨‍💻 Author

Built by **sunshine**

---

## ⭐️ Support

If you find this project helpful, consider giving it a ⭐️ on GitHub!
