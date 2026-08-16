# 🍽️ Restaurant Management System (Python & PostgreSQL)

A console-based **Restaurant Management System** built with Python and PostgreSQL. This project handles menu management, table tracking, order processing, and daily sales reporting.

---

## ✨ Features

1. **Menu Management**: Add new food items and update item prices.
2. **Table Management**: View table statuses, add new tables, update table status (`available`/`occupied`), and remove empty tables.
3. **Order Management**: Create new orders for available tables, add multiple items with quantities, and update order statuses (`received`, `preparing`, `ready`, `paid`).
4. **Reports & Analytics**: View active orders, inspect detailed order receipts with calculated totals using `JOIN` queries, and generate daily sales reports with date tracking.
5. **Error Handling**: Comprehensive input validation and business logic constraints (e.g., preventing orders on occupied tables, removing occupied tables, or entering invalid item IDs).

---

## 🛠️ Prerequisites

Make sure you have the following installed on your system:
- **Python** (v3.x recommended)
- **PostgreSQL**

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ZahraAghaeii/daneshkar_database_restaurant.git
cd restaurant_project

```

### 2. Set Up Virtual Environment

* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **Mac / Linux:**
```bash
python -m venv venv
source venv/bin/activate

```



### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Database Configuration

1. Open your PostgreSQL console or **pgAdmin**.
2. Create a new database named `restaurant_db`:
```sql
CREATE DATABASE restaurant_db;

```


3. Run the queries provided in `schema.sql` inside your database to create the required tables and initial items.

### 5. Configure Database Connection

Open `app.py` and update your PostgreSQL credentials in the `get_connection()` function:

```python
def get_connection():
    return psycopg2.connect(
        dbname="restaurant_db",
        user="postgres",
        password="20041382",  # Replace with your PostgreSQL password
        host="localhost",
        port="5432"
    )

```

### 6. Run the Application

```bash
python app.py

```

---

## 📁 Project Structure

```text
restaurant_project/
│
├── app.py              # Main application logic and CLI interface
├── schema.sql          # Database creation and table schemas
├── requirements.txt    # Project dependencies (psycopg2-binary)
└── README.md           # Project documentation

```

---

## 📄 License

This project is developed as an academic assignment.



