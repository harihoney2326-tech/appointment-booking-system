# Appointment Booking System (Django + SQLite/MySQL)

A simple Doctor Appointment Booking System with:
- Patient registration & login
- Doctor listing
- Book appointment (date & time, with double-booking prevention)
- My Appointments page (view/cancel)
- Admin panel to manage Doctors and Appointment status

---

## 🚀 Setup Steps (run these in order)

### 1. Install Python
Make sure Python 3.10+ is installed. Check with:
```
python --version
```

### 2. Create & activate a virtual environment
```
python -m venv venv
```
Windows:
```
venv\Scripts\activate
```
Mac/Linux:
```
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create the database tables
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an admin (superuser) account
```
python manage.py createsuperuser
```
Enter username, email, password when asked.

### 6. Run the server
```
python manage.py runserver
```
Open browser: **http://127.0.0.1:8000/**

### 7. Add doctors (important!)
Go to **http://127.0.0.1:8000/admin/**, login with superuser, click on
**Doctors → Add Doctor**, and add 2-3 sample doctors (name, specialization,
available days, timings, fee).

### 8. Test the flow
- Go back to homepage → Register as a patient → Login
- Click "Doctors" → Book Appointment → choose date/time → Confirm
- Check "My Appointments" page

---

## 🔄 Switching from SQLite to MySQL (optional, for final submission)

1. Install MySQL Server + create a database:
   ```sql
   CREATE DATABASE appointment_db;
   ```
2. Install the MySQL driver:
   ```
   pip install mysqlclient
   ```
3. In `appointment_system/settings.py`, replace the `DATABASES` block with:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'appointment_db',
           'USER': 'root',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
4. Run migrations again:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## 📁 Project Structure
```
appointment_system/
├── manage.py
├── requirements.txt
├── appointment_system/      ← project settings, urls
└── booking/                 ← main app
    ├── models.py            ← Doctor, Appointment tables
    ├── views.py              ← business logic
    ├── forms.py               ← registration & booking forms
    ├── admin.py                ← admin panel config
    ├── urls.py
    └── templates/             ← all HTML pages (Bootstrap styled)
```

## 🧠 For your project report / viva
- **ER Diagram entities:** User (Django built-in) — Patient, Doctor, Appointment
- **Relationships:** One Doctor → many Appointments | One Patient(User) → many Appointments
- **Key logic to highlight:** `unique_together` on (doctor, date, time) in `models.py`
  prevents double-booking at the database level — good talking point in viva.
- **Possible extensions (mention as "future scope"):** Email/SMS reminders,
  doctor login to confirm/reject appointments, payment integration, ratings/reviews.
