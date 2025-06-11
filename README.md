
# Demo Project

<p align="center">
  <img src="./assets/logo.png" alt="DemoProject Logo" width="250" />
</p>

<div align="center">
  
  ![Django CI](https://github.com/ihoooman/demoproject/actions/workflows/ci.yml/badge.svg)
  ![License](https://img.shields.io/github/license/ihoooman/demoproject.svg)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
  ![Issues](https://img.shields.io/github/issues/ihoooman/demoproject.svg)
  </img> <img src="https://img.shields.io/badge/deployed%20on-Railway-7B16FF.svg" alt="Deployed on Railway"></img>



</div>

> A comprehensive Django-based survey and assessment management system for creating hierarchical groups, categories, and subcategories to organize questions and collect responses.

![System Screenshot](screenshots/demo.png)

## 🚀 Overview

This project is a powerful Django-based application for user management, survey, and assessment. It enables you to build hierarchical groups, categories, subcategories, organize questions, collect responses, and efficiently manage user access. It comes with custom authentication, flexible upload center, a modern dashboard, and robust CI/CD integration.

---

## ✨ Key Features

- **Advanced Authentication**
  - Custom user model (supports both email and phone)
  - Google OAuth login (django-allauth)
  - Phone verification using Kavenegar SMS API
  - User activation and multi-factor authentication

* **Upload Center**
  * Upload center for images and media files
  * Secure storage and management of uploaded content
  * Store images, documents, and other media
  * Easy access to uploaded content in forms and responses

* **Hierarchical Organization**

  * Define groups with parent–child relationships
  * Organize content into categories and nested subcategories
  * Adaptable structure for quizzes, polls, and assessments

- **Survey & Response Management**
  
  - Create multiple types of questions (checklist, multiple choice, etc.)
  - Store and filter responses by user, group, category, subcategory
  - Export responses for reporting and analytics


* **Dashboard Interface**

  * Intuitive UI for browsing hierarchy and managing content
  * Dynamic forms for submitting survey responses
  * Admin views for bulk operations and content moderation

- **Powerful API**
   
  - RESTful API built with Django REST Framework (DRF)
  - Ready endpoints for groups, categories, questions, and responses
  - Modular and clean codebase for easy extension

- **CI/CD & Deployment**
  - Fully automated deployment to Railway via GitHub Actions
  - Automated testing and code quality checks on each push

---

## 🛠 Technologies Used

| Layer              | Tools & Libraries                             |
| ------------------ |-----------------------------------------------|
| **Backend**        | Django 5.2.1, Python 3.x, PostgreSQL          |
| **Authentication** | django-allauth, custom phone auth             |
| **Frontend**       | Django Templates, HTML5, CSS3, JavaScript     |
| **APIs**        | Django REST Framework, Google OAuth, Kavenegar SMS API |
| **DevOps**      | Docker, Docker Compose, Railway, GitHub Actions |


---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ihoooman/demoproject.git
   cd survey-management-system
   ```
2. **Set up a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
      
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

   * Copy `.env.example` to `.env` and update keys:

     ```env
     SECRET_KEY=your_secret_key
     KAVENEGAR_API_KEY=your_api_key
     LOWERCASE_DOMAIN=yourdomain.com
     ```
5. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```
6. **Create a superuser** (optional)

   ```bash
   python manage.py createsuperuser
   ```
7. **Start the development server**

   ```bash
   python manage.py runserver
   ```
8. **Visit** `http://127.0.0.1:8000/` in your browser.

---

## 🐳 Docker Deployment

You can also run this application using Docker, which simplifies the setup process and ensures consistency across different environments.

### Using Docker

1. **Build and run with Docker**

   ```bash
   # Build the Docker image
   docker build -t survey-management-system .

   # Run the container
   docker run -p 8000:8000 survey-management-system
   ```

2. **Using Docker Compose** (recommended)

   ```bash
   # Start all services
   docker-compose up

   # Run in detached mode
   docker-compose up -d

   # Stop all services
   docker-compose down
   ```

3. **Access the application**

   Visit `http://localhost:8000` in your browser.

### Environment Variables

When using Docker, you can configure the application by setting environment variables in the `docker-compose.yml` file or by passing them to the `docker run` command:

```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your_secret_key \
  -e ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com \
  survey-management-system
```

---

## 🔧 Configuration

### Google OAuth

1. Create a project in the [Google Cloud Console](https://console.developers.google.com/).
2. Enable **Google+ API** and generate OAuth credentials.
3. Add your application domain to **Authorized domains**.
4. Update `SOCIALACCOUNT_PROVIDERS` in `settings.py`:

   ```python
   SOCIALACCOUNT_PROVIDERS = {
       'google': {
           'APP': {
               'client_id': 'YOUR_CLIENT_ID',
               'secret': 'YOUR_CLIENT_SECRET',
           }
       }
   }
   ```

### Kavenegar SMS API

1. Sign up at [Kavenegar](https://kavenegar.com/) and obtain an API key.
2. Set `KAVENEGAR_API_KEY` and `KAVENEGAR_SENDER` in `.env`:

   ```env
   KAVENEGAR_API_KEY=your_api_key
   KAVENEGAR_SENDER=your_sender_number
   ```

---
## 🚀 Deployment
This application is deployed on Railway with continuous deployment set up via GitHub Actions.

Live Demo: 
   ```
https://demoproject-production-6b92.up.railway.app
   ```
The deployment workflow automatically triggers a rebuild on Render when changes are pushed to the main branch.


---


## 📂 Project Structure


```plaintext
demoproject/
├── LICENSE
├── README.md
├── requirements.txt
├── .env.example
├── manage.py
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── tests.py
├── dashboard/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── tests.py
│   └── templates/
│       └── dashboard/
├── login/
│   └── utils.py
├── screenshots/
│   └── demo.png
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a branch: `git checkout -b feature/YourFeature`
3. Commit: `git commit -m "Add YourFeature"`
4. Push: `git push origin feature/YourFeature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---


## 📌 Latest Commit

- **SHA:** [`20aeb115`](https://github.com/ihoooman/demoproject/commit/20aeb115918c96a338a1666dab9891a9d9d03e7a)
- **Author:** Hooman Maddah ([ihoooman](https://github.com/ihoooman))
- **Date:** 2025-06-11 11:01 UTC
- **Message:** Add djangorestframework version 3.16.0 to requirements.txt

---

Thank you for using and contributing! 🌟

## 🙋‍♂️ Contact & Showcase

* **GitHub**: [github.com/ihoooman](https://github.com/ihoooman)
* **LinkedIn**: [linkedin.com/in/hoomanmdd](https://linkedin.com/in/hoomanmdd)

Feel free to explore, review, or connect!
