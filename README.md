# GardeningCareServicesApp
My Django project for SoftUni Python web - september 2024 final
A basic web app for sharing gardening services. Users can browse listed services by registered providers. If they are logged in can rate and comment services.
In the app are implemented moderation roles for easy comment, and profile management.  
---

## General Requirements
- **Python**: Version 3.12 or higher.
- **PostgreSQL**: Database.
- **pip**: For installing dependencies.
- **Browser**: A Chromium-based browser is recommended but others probably work as well.
- **GIT**: Alternatively you can just download the source code.
- **Python Virtual Environment**: Optional, but recommended.
---

## Setup Instructions

### Step 1: Clone the project
```bash
https://github.com/DelyanNikolov/GardeningCareServicesApp.git
```


### Step 2: Install Dependencies


You must install required project libraries:
```bash
pip install -r requirements.txt
```

### Step 3: Create a `.env` File
At the root level of the project (where `manage.py` is located), create a `.env` file using this template:
```env
# Django secret key
# I know this is a security issue but the project is late and i must show part of the secret info
# Sorry I should hide my secrets early

SECRET_KEY=django-insecure-78_fhen6h0!_ki!5w7@cnv((^y$h8)qumwlsi1w(4(a)pein9b

# Debug mode
DEBUG=True

# PostgreSQL database settings
DB_NAME=your_db_name
DB_USER=postgres
DB_PASSWORD=your_postgres_user_password
DB_HOST=127.0.0.1
DB_PORT=5432


### Step 3: Database Migration
Run migrations with this command:
```bash
python manage.py migrate
```


### Step 4: Run the app locally
Use this command to run the app:
```bash
python manage.py runserver
```
With a browser open:
http://localhost:8000/
---

## User Roles and Permissions

The web app features the following users, each with its own permissions:

### 1. Anonymous Users
- View and search services, view providers profiles.
- Register and sign in.

### 2. Homeowner users:
- All anonymous user permissions.
- Can Edit/Delete their profile in the app.
- Only one comment and rating per profile.

### 3. Service provider users
- All anonymous user permissions.
- Can Edit/Delete their profile in the app.
- Can Add/Edit/Delete their services in their profile page.
- They can not comment or rate gardening services.

### 4. Moderators  (users with the moderator permissions )
- Review and approve or delete comments.
- Their default home page is moderation dashboard.
- Can add or remove categories for the services.

### 5. Administrators (users with the Administrator permissions )
- All moderator permissions.
- Can edit or delete Service provider profiles.


### 6. Superuser
- All staff permissions.
- Full CRUD on all users, services, categories, and reviews.

---

## Testing User Accounts

### Groups:  
#### (Prefilled for testing on production only)
#### Moderators
- CRUD operations for reviews.
- CRUD operations for Service category.

#### Administrators
- All Moderators permissions.
- CRUD operations for Homeowner profiles.
- CRUD operations for Service provider profiles.
- CRUD operations for Services.


Pre-generated user accounts are provided for testing purposes (on production only):

| Role                 | Email                        | Password  |
|----------------------|------------------------------|-----------|
| Superuser            | admin@admin.com              | admin     |
| Homeownrer           | homeowner@test.com           | 12home34  |
| Provider             | provider@test.com            | 12test34  |
| Moderator            | moderator@test.com           | 12moder34 |
| Administrator        | administrator@test.com       | 12admin34 |

---

## Features

### General Features
- **Dynamic Homepage**: Displays public home or moderation for users with different permissions.
- **Services Search**: Basic search bar.
- **Pagination**: Available on multiple pages.
- **Create/Edit/Delete** Service category build with REST.

### Security
- Secure permissions with checks and permission mixins.
- User-uploaded images are validated.

### Custom Admin Site
- Easy groups, permissions and roles management.
- Advanced filtering and search options.

### Tests
- Phone number validator tests.
- Services views: approve review, service, delete, service details.
