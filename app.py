import psycopg2
from datetime import datetime

def get_connection():
    return psycopg2.connect(
        dbname="restaurant_db",
        user="postgres",
        password="20041382",  
        host="localhost",
        port="5432"
    )

# ======================
# مدیریت منو : بخش ۱
# ======================

def add_menu_item():
    name = input("Enter food name: ").strip()
    if not name:
        print("Error: Food name cannot be empty.")
        return
    
    try:
        price = float(input("Enter food price: "))
        if price < 0:
            print("Error: Price cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid price format.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO menu_items (name, price) VALUES (%s, %s)", (name, price))
        conn.commit()
        print(f"Menu item '{name}' added successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def edit_menu_item_price():
    show_menu()
    try:
        item_id = int(input("Enter item ID to edit: "))
        new_price = float(input("Enter new price: "))
        if new_price < 0:
            print("Error: Price cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid input.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE menu_items SET price = %s WHERE id = %s", (new_price, item_id))
        if cur.rowcount == 0:
            print("Error: Item ID not found.")
        else:
            conn.commit()
            print("Price updated successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def show_menu():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM menu_items")
    items = cur.fetchall()
    cur.close()
    conn.close()

    print("\n========= MENU =========")
    print(f"{'ID':<4} {'Name':<15} {'Price'}")
    print("-" * 35)
    for item in items:
        print(f"{item[0]:<4} {item[1]:<15} {item[2]}")
    print("===============================")

# ======================
# مدیریت میزها : بخش ۲
# ======================

def show_tables_status():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT table_number, status FROM tables ORDER BY table_number")
    tables = cur.fetchall()
    cur.close()
    conn.close()

    print("\n========= Tables =========")
    print(f"{'Table':<8} {'Status'}")
    print("-" * 25)
    for t in tables:
        print(f"{t[0]:<8} {t[1]}")
    print("=============================")

def update_table_status():
    show_tables_status()
    try:
        table_number = int(input("Enter table number to update: "))
    except ValueError:
        print("Error: Invalid input.")
        return
        
    new_status = input("Enter new status (available/occupied): ").strip().lower()
    if new_status not in ['available', 'occupied']:
        print("Error: Status must be 'available' or 'occupied'.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE tables SET status = %s WHERE table_number = %s", (new_status, table_number))
        if cur.rowcount == 0:
            print("Error: Table not found.")
        else:
            conn.commit()
            print(f"Table #{table_number} status updated to {new_status}.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def add_table():
    try:
        table_number = int(input("Enter new table number: "))
    except ValueError:
        print("Error: Invalid table number.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO tables (table_number, status) VALUES (%s, 'available')", (table_number,))
        conn.commit()
        print(f"Table #{table_number} added successfully!")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print(f"Error: Table #{table_number} already exists.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def remove_table():
    show_tables_status()
    try:
        table_number = int(input("Enter table number to remove: "))
    except ValueError:
        print("Error: Invalid input.")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT status FROM tables WHERE table_number = %s", (table_number,))
        result = cur.fetchone()
        if not result:
            print("Error: Table not found.")
            return
        
        if result[0] == 'occupied':
            print(f"Error: Table #{table_number} is currently occupied and cannot be removed.")
            return

        cur.execute("DELETE FROM tables WHERE table_number = %s", (table_number,))
        conn.commit()
        print(f"Table #{table_number} removed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

# ======================
# مدیریت سفارش‌ها : بخش ۳
# ======================

def add_order():
    show_tables_status()
    try:
        table_num = int(input("Enter table number for the new order: "))
    except ValueError:
        print("Error: Invalid table number.")
        return

    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, status FROM tables WHERE table_number = %s", (table_num,))
    table_data = cur.fetchone()
    
    if not table_data:
        print("Error: Table does not exist.")
        cur.close()
        conn.close()
        return
    
    table_id, table_status = table_data
    if table_status == 'occupied':
        print(f"Error: Table #{table_num} is currently occupied. Please choose another table.")
        cur.close()
        conn.close()
        return

    print(f"Starting new order for Table #{table_num}...")
    
    cur.execute("UPDATE tables SET status = 'occupied' WHERE id = %s", (table_id,))
    cur.execute("INSERT INTO orders (table_id, status) VALUES (%s, 'preparing') RETURNING id", (table_id,))
    order_id = cur.fetchone()[0]
    
    show_menu()
    
    while True:
        try:
            item_id = int(input("Enter item ID to add (or 0 to finish): "))
            if item_id == 0:
                break
            
            cur.execute("SELECT name FROM menu_items WHERE id = %s", (item_id,))
            item = cur.fetchone()
            if not item:
                print("Error: Invalid item ID.")
                continue
                
            quantity = int(input(f"Enter quantity for {item[0]}: "))
            if quantity <= 0:
                print("Error: Quantity must be greater than 0.")
                continue
                
            cur.execute("INSERT INTO order_details (order_id, item_id, quantity) VALUES (%s, %s, %s)", 
                        (order_id, item_id, quantity))
            conn.commit()
            print(f"Added: {item[0]} (x{quantity})")
        except ValueError:
            print("Error: Invalid input.")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Order #{order_id} created successfully for Table #{table_num}!")

def update_order_status():
    try:
        order_id = int(input("Enter Order ID: "))
    except ValueError:
        print("Error: Invalid ID.")
        return

    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT status, table_id FROM orders WHERE id = %s", (order_id,))
    order = cur.fetchone()
    if not order:
        print("Error: Order not found.")
        cur.close()
        conn.close()
        return
        
    current_status, table_id = order
    print(f"Current status: {current_status}")
    print("Select new status:\n1. received\n2. preparing\n3. ready\n4. paid")
    
    choice = input("Your choice: ")
    status_map = {"1": "received", "2": "preparing", "3": "ready", "4": "paid"}
    
    if choice not in status_map:
        print("Error: Invalid choice.")
        cur.close()
        conn.close()
        return
        
    new_status = status_map[choice]
    cur.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
    
    if new_status == 'paid':
        cur.execute("UPDATE tables SET status = 'available' WHERE id = %s", (table_id,))
        print(f"\nOrder #{order_id} marked as PAID.")
        print(f"Table is now AVAILABLE again.")
    else:
        print(f"\nOrder #{order_id} status updated to {new_status}.")
        
    conn.commit()
    cur.close()
    conn.close()

# ======================
# گزارش‌گیری : بخش ۴
# ======================

def show_active_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, t.table_number, o.status, o.order_time 
        FROM orders o 
        JOIN tables t ON o.table_id = t.id 
        WHERE o.status != 'paid'
    """)
    orders = cur.fetchall()
    cur.close()
    conn.close()

    print("\n========= Active Orders =========")
    for o in orders:
        print(f"Order #{o[0]} | Table #{o[1]} | Status: {o[2]} | Time: {o[3]}")
    print("====================================")

def show_order_details():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT o.id, t.table_number, o.status, o.order_time 
        FROM orders o 
        JOIN tables t ON o.table_id = t.id 
        ORDER BY o.id
    """)
    all_orders = cur.fetchall()
    
    if not all_orders:
        print("\nNo orders found in the system.")
        cur.close()
        conn.close()
        return

    print("\n========= All Orders List =========")
    print(f"{'Order ID':<10} {'Table':<8} {'Status':<12} {'Time'}")
    print("-" * 45)
    for ord_row in all_orders:
        print(f"#{ord_row[0]:<9} #{ord_row[1]:<7} {ord_row[2]:<12} {ord_row[3]}")
    print("======================================")

    try:
        order_id = int(input("Enter Order ID to view details: "))
    except ValueError:
        print("Error: Invalid ID.")
        cur.close()
        conn.close()
        return
    
    cur.execute("""
        SELECT o.status, t.table_number 
        FROM orders o 
        JOIN tables t ON o.table_id = t.id 
        WHERE o.id = %s
    """, (order_id,))
    order_info = cur.fetchone()
    
    if not order_info:
        print("Error: Order not found.")
        cur.close()
        conn.close()
        return

    status, table_number = order_info

    cur.execute("""
        SELECT m.name, od.quantity, m.price, (od.quantity * m.price) as total
        FROM order_details od
        JOIN menu_items m ON od.item_id = m.id
        WHERE od.order_id = %s
    """, (order_id,))
    details = cur.fetchall()
    
    cur.close()
    conn.close()

    print(f"\n========= Order #{order_id} =========")
    print(f"{'Item':<12} {'Qty':<6} {'Price':<10} {'Total'}")
    print("-" * 40)
    grand_total = 0
    for d in details:
        print(f"{d[0]:<12} {d[1]:<6} {d[2]:<10} {d[3]}")
        grand_total += d[3]
    print("-" * 40)
    print(f"Total: {grand_total}")
    print(f"Status: {status}")
    print(f"Table: #{table_number}")
    print("===============================")

def get_daily_sales_report():
    conn = get_connection()
    cur = conn.cursor()
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    cur.execute("""
        SELECT 
            COUNT(*),
            SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status != 'paid' THEN 1 ELSE 0 END)
        FROM orders 
        WHERE DATE(order_time) = CURRENT_DATE
    """)
    order_stats = cur.fetchone()
    
    cur.execute("""
        SELECT SUM(od.quantity * m.price)
        FROM orders o
        JOIN order_details od ON o.id = od.order_id
        JOIN menu_items m ON od.item_id = m.id
        WHERE o.status = 'paid' AND DATE(o.order_time) = CURRENT_DATE
    """)
    total_sales = cur.fetchone()[0] or 0
    
    cur.close()
    conn.close()

    print("\n========= Daily Sales =========")
    print(f"Date: {today_date}\n")  
    print(f"Total Orders: {order_stats[0] or 0}")
    print(f"Paid Orders: {order_stats[1] or 0}")
    print(f"Unpaid Orders: {order_stats[2] or 0}\n")
    print(f"Total Sales: {total_sales:,.0f}")
    print("===============================")
    
# ======================
# رابط کاربری (CLI)
# ======================

def manage_menu_items():
    while True:
        print("\n--- Menu Management ---")
        print("1. Add a new menu item")
        print("2. Edit menu item price")
        print("3. Back to main menu")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_menu_item()
        elif choice == "2":
            edit_menu_item_price()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

def manage_tables_menu():
    while True:
        print("\n--- Table Management ---")
        print("1. Add a new table")
        print("2. Remove a table")
        print("3. Update Table Status")
        print("4. Back to main menu")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_table()
        elif choice == "2":
            remove_table()
        elif choice == "3":
            update_table_status()
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

def main_menu():
    while True:
        print("\n=========================================")
        print(" Restaurant Management System")
        print("=========================================")
        print("1. Show Menu")
        print("2. Show Table Status")
        print("3. Add New Order")
        print("4. Update Order Status")
        print("5. View Order Details & Total Price")
        print("6. Show Daily Sales Report")
        print("7. Manage Menu")          
        print("8. Manage Tables")        
        print("9. Exit")                
        print("-----------------------------------------")
        
        choice = input("Please select an option (1-9): ")
        
        if choice == "1":
            show_menu()
        elif choice == "2":
            show_tables_status()
        elif choice == "3":
            add_order()
        elif choice == "4":
            update_order_status()
        elif choice == "5":
            show_order_details()
        elif choice == "6":
            get_daily_sales_report()
        elif choice == "7":
            manage_menu_items()     
        elif choice == "8":
            manage_tables_menu()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()