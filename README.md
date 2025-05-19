
# Survey Management System

> A comprehensive Django-based survey and assessment management system for creating hierarchical groups, categories, and subcategories to organize questions and collect responses.

![System Screenshot](screenshots/demo.png)

## 🚀 Overview

The **Survey Management System** is designed to help organizations build flexible, hierarchical survey structures and gather insights efficiently. This demo project showcases best practices in Django application design, authentication, API integration, and user-friendly dashboards.

---

## 🎯 Key Features

* **User Authentication**

  * Custom user model supporting email and phone number
  * Social login via Google OAuth (django-allauth)
  * Phone verification with SMS (Kavenegar API)

* **Hierarchical Organization**

  * Define groups with parent–child relationships
  * Organize content into categories and nested subcategories
  * Adaptable structure for quizzes, polls, and assessments

* **Response Collection**

  * Record and store user answers to various question types
  * Filter and track responses by user, group, category, and subcategory
  * Exportable data for reporting and analysis

* **Dashboard Interface**

  * Intuitive UI for browsing hierarchy and managing content
  * Dynamic forms for submitting survey responses
  * Admin views for bulk operations and content moderation

---

## 🛠 Technologies Used

| Layer              | Tools & Libraries                         |
| ------------------ | ----------------------------------------- |
| **Backend**        | Django 5.2.1, Python 3.x, SQLite          |
| **Authentication** | django-allauth, custom phone auth         |
| **Frontend**       | Django Templates, HTML5, CSS3, JavaScript |
| **APIs**           | Google OAuth REST API, Kavenegar SMS API  |

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

## 📂 Project Structure

```plaintext
survey-management-system/
├── LICENSE
├── README.md
├── requirements.txt
├── .env.example
├── manage.py
├── .gitignore
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
│           ├── group_list.html
│           └── subcategory_list.html
├── login/
│   └── utils.py
└── screenshots/
    └── demo.png
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

## 🙋‍♂️ Contact & Showcase

* **GitHub**: [github.com/ihoooman](https://github.com/ihoooman)
* **LinkedIn**: [linkedin.com/in/hoomanmdd](https://linkedin.com/in/hoomanmdd)

Feel free to explore, review, or connect!
