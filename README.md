# Multi-Vendor Marketplace with Django

A complete final-year project blueprint for building a multi-vendor marketplace where multiple sellers list products and buyers place orders.

---

# 1. Project Overview

## Project Title

VendorHub – Multi-Vendor Marketplace

## Objective

Build an e-commerce platform where:

* Vendors register and manage products.
* Customers browse and purchase products.
* Orders are split by vendor.
* Payments are processed online.
* Each vendor sees their own dashboard.
* Admin manages users, products, and commissions.

---

# 2. Tech Stack

## Backend

* Django
* Django REST Framework (optional for APIs)

## Database

* MySQL

## Frontend

* Django Templates + Bootstrap

## Payment Gateway

* Razorpay

## Media Storage

* Local during development
* AWS S3 (optional for production)

## Deployment

* Render / Railway / AWS

---

# 3. User Roles

1. Admin
2. Vendor (Seller)
3. Customer (Buyer)

---

# 4. Core Features

## Customer Features

* Register/Login
* Browse products
* Search and filter
* Add to cart
* Checkout and payment
* Order history
* Track order status

## Vendor Features

* Register as vendor
* Add/edit/delete products
* Manage stock
* View orders for their products
* Update order status
* Dashboard with revenue and sales

## Admin Features

* Approve vendors
* Manage categories
* Manage products
* View all orders
* Set commission percentages

---

# 5. Database Design

## CustomUser

* id
* username
* email
* password
* role (admin, vendor, customer)
* phone

## VendorProfile

* user (OneToOne)
* store_name
* description
* logo
* address
* approved

## Category

* name
* slug

## Product

* vendor (ForeignKey)
* category (ForeignKey)
* name
* slug
* description
* price
* stock
* image
* active
* created_at

## Cart

* user
* created_at

## CartItem

* cart
* product
* quantity

## Order

* user
* total_amount
* payment_id
* status
* created_at

## OrderItem

* order
* product
* vendor
* quantity
* price
* status

## Payment

* order
* razorpay_order_id
* razorpay_payment_id
* amount
* status

## Review

* user
* product
* rating
* comment

---

# 6. Django Apps Structure

```text
vendorhub/
├── accounts/
├── vendors/
├── products/
├── cart/
├── orders/
├── payments/
├── reviews/
├── dashboard/
├── templates/
├── static/
├── media/
└── vendorhub/
```

---

# 0. Beginner-Friendly Windows Setup Guide

This section explains exactly what to install first and how to start the project on a Windows laptop.

---

## Step 1: Install Required Software

Install these tools in order:

### 1. Python

* Download Python 3.12 or later from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* During installation, check **Add Python to PATH**.

### 2. Visual Studio Code

* Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
* Recommended extensions:

  * Python
  * Django
  * Pylance

### 3. Git

* Download from [https://git-scm.com/](https://git-scm.com/)

### 4. MySQL Community Server

* Download from [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
* Set a root password and remember it.

### 5. MySQL Workbench (optional but recommended)

* GUI tool for viewing your database.

### 6. Google Chrome

* Useful for testing the web application.

---

## Step 2: Verify Installation

Open Command Prompt and run:

```bash
python --version
pip --version
git --version
mysql --version
```

If version numbers are displayed, installation is successful.

---

## Step 3: Create Project Folder

```bash
mkdir vendorhub_project
cd vendorhub_project
```

---

## Step 4: Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of the command line.

---

## Step 5: Install Required Python Packages

```bash
pip install django mysqlclient pillow razorpay python-dotenv
```

If `mysqlclient` fails to install, use:

```bash
pip install PyMySQL
```

---

## Step 6: Create MySQL Database

Open MySQL Command Line Client and run:

```sql
CREATE DATABASE vendorhub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## Step 7: Create Django Project

```bash
django-admin startproject vendorhub .
```

The dot (`.`) creates the project in the current folder.

---

## Step 8: Create Django Apps

```bash
python manage.py startapp accounts
python manage.py startapp vendors
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
python manage.py startapp payments
python manage.py startapp reviews
python manage.py startapp dashboard
```

---

## Step 9: Open Project in VS Code

```bash
code .
```

---

## Step 10: Configure Database in settings.py

Replace the `DATABASES` setting with the MySQL configuration shown later in this document.

---

## Step 11: Register Apps in settings.py

Add to `INSTALLED_APPS`:

```python
'accounts',
'vendors',
'products',
'cart',
'orders',
'payments',
'reviews',
'dashboard',
```

---

## Step 12: Create Custom User Model

Write the `accounts/models.py` code from this document.

---

## Step 13: Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 14: Create Admin User

```bash
python manage.py createsuperuser
```

Enter username, email, and password.

---

## Step 15: Run Development Server

```bash
python manage.py runserver
```

Open:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Step 16: Login to Admin Panel

Use the superuser credentials created above.

---

## Step 17: Begin Development in This Order

1. Custom User Model
2. Vendor Profile
3. Product and Category Models
4. Admin Registration
5. Authentication (signup/login)
6. Product Listing Pages
7. Cart
8. Checkout
9. Razorpay Integration
10. Order Tracking
11. Vendor Dashboard
12. Deployment

---

## Recommended Daily Workflow

Each time you work on the project:

```bash
cd vendorhub_project
venv\Scripts\activate
python manage.py runserver
```

When you change models:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## First Week Goal

By the end of week 1, you should have:

* Python and MySQL installed
* Django project created
* Database connected
* Custom user model working
* Admin panel accessible

---

## Common Windows Commands

### Activate virtual environment

```bash
venv\Scripts\activate
```

### Deactivate virtual environment

```bash
deactivate
```

### Install packages

```bash
pip install package_name
```

### Start server

```bash
python manage.py runserver
```

### Stop server

Press `Ctrl + C`

---

## Troubleshooting

### Python not recognized

Reinstall Python and check **Add Python to PATH**.

### mysqlclient installation error

Install `PyMySQL` instead.

### Port 8000 already in use

Run:

```bash
python manage.py runserver 8001
```

---

# 7. Project Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate

### Windows

```bash
venv\Scripts\activate
```

## Install Packages

```bash
pip install django mysqlclient pillow razorpay
```

## Start Project

```bash
django-admin startproject vendorhub
cd vendorhub
```

## Create Apps

```bash
python manage.py startapp accounts
python manage.py startapp vendors
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
python manage.py startapp payments
python manage.py startapp reviews
python manage.py startapp dashboard
```

---

# 8. MySQL Configuration

In `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vendorhub',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

---

# 9. Custom User Model

## accounts/models.py

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
```

## settings.py

```python
AUTH_USER_MODEL = 'accounts.User'
```

---

# 10. Vendor Model

## vendors/models.py

```python
from django.db import models
from django.conf import settings

class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='vendors/', blank=True, null=True)
    address = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name
```

---

# 11. Product Model

## products/models.py

```python
from django.db import models
from vendors.models import VendorProfile

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Product(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

---

# 12. Cart Workflow

1. Customer adds product to cart.
2. CartItem stores quantity.
3. Cart total is calculated dynamically.
4. Checkout creates Order and OrderItems.

---

# 13. Order Workflow

1. Customer checks out.
2. Create Razorpay order.
3. Payment is completed.
4. Save payment details.
5. Create Order and OrderItems.
6. Notify vendors.
7. Vendors update shipping status.

---

# 14. Razorpay Integration

## Install

```bash
pip install razorpay
```

## Settings

```python
RAZORPAY_KEY_ID = 'your_key_id'
RAZORPAY_KEY_SECRET = 'your_secret'
```

## Create Client

```python
import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)
```

## Create Razorpay Order

```python
payment = client.order.create({
    'amount': 50000,  # paise
    'currency': 'INR',
    'payment_capture': 1,
})
```

---

# 15. Seller Dashboard Metrics

Show:

* Total Products
* Total Orders
* Revenue
* Pending Orders
* Low Stock Products

---

# 16. Customer Pages

* Home
* Product List
* Product Detail
* Cart
* Checkout
* Payment Success
* Order History
* Profile

---

# 17. Vendor Pages

* Vendor Registration
* Vendor Dashboard
* Product CRUD
* Orders List
* Earnings Report

---

# 18. Admin Pages

Use Django Admin for:

* Vendor approvals
* Category management
* Order monitoring
* User management

---

# 19. Authentication

Use Django authentication:

* Signup
* Login
* Logout
* Password reset

Decorators:

* `login_required`
* custom role-based checks

---

# 20. Search and Filters

* Search by product name
* Filter by category
* Price range filter
* Sort by price/date

---

# 21. Reviews and Ratings

Customers can:

* Give 1–5 stars
* Write comments
* View average rating

---

# 22. Security

* CSRF protection
* Input validation
* Login required for checkout
* Payment signature verification

---

# 23. Development Roadmap

## Phase 1: Setup

* Create project and apps
* Configure MySQL
* Create custom user model

## Phase 2: Authentication

* Signup/login/logout
* Role-based registration

## Phase 3: Vendor Module

* Vendor profile
* Approval workflow

## Phase 4: Product Module

* Categories
* Product CRUD

## Phase 5: Marketplace

* Product listing and detail pages
* Search and filters

## Phase 6: Cart and Checkout

* Add/remove cart items
* Checkout

## Phase 7: Payments

* Razorpay integration
* Payment verification

## Phase 8: Orders

* Order creation and tracking

## Phase 9: Dashboards

* Vendor analytics
* Customer history

## Phase 10: Deployment

* Static/media configuration
* Production settings

---

# 24. Suggested Timeline (6 Weeks)

## Week 1

Setup, MySQL, authentication

## Week 2

Vendor registration and approvals

## Week 3

Products and categories

## Week 4

Cart and checkout

## Week 5

Razorpay and order management

## Week 6

Dashboards, testing, deployment

---

# 25. Optional Advanced Features

* Wishlist
* Coupons
* Commission calculations
* Email notifications
* PDF invoices
* REST API
* Mobile app integration
* Recommendation system

---

# 26. Resume Description

Developed a multi-vendor marketplace using Django and MySQL where sellers manage products and customers purchase online using Razorpay. Implemented role-based authentication, cart and checkout, order tracking, reviews, and vendor analytics dashboards.

---

# 27. GitHub Repository Structure

```text
README.md
requirements.txt
.env
.gitignore
vendorhub/
```

---

# 28. requirements.txt

```text
Django
mysqlclient
Pillow
razorpay
python-dotenv
```

---

# 29. Deployment Checklist

* DEBUG = False
* ALLOWED_HOSTS configured
* MySQL production database
* Static files collected
* Environment variables set
* HTTPS enabled

---

