
import sqlite3

# Database connection
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

conn.commit()


# Add Product
def add_product():
    print("\n--- Add New Product ---")

    name = input("Enter product name: ")
    category = input("Enter category: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    if quantity < 0 or price < 0:
        print("Quantity and price cannot be negative.")
        return

    cursor.execute("""
    INSERT INTO products (name, category, quantity, price)
    VALUES (?, ?, ?, ?)
    """, (name, category, quantity, price))

    conn.commit()
    print("Product added successfully!")


# View Products
def view_products():
    print("\n--- Product List ---")

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if not products:
        print("No products available.")
        return

    print("-" * 75)
    print("{:<5} {:<20} {:<15} {:<10} {:<10}".format(
        "ID", "Name", "Category", "Quantity", "Price"
    ))
    print("-" * 75)

    for product in products:
        print("{:<5} {:<20} {:<15} {:<10} {:<10.2f}".format(
            product[0], product[1], product[2],
            product[3], product[4]
        ))


# Search Product
def search_product():
    print("\n--- Search Product ---")

    name = input("Enter product name: ")

    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    products = cursor.fetchall()

    if products:
        for product in products:
            print(product)
    else:
        print("Product not found.")


# Update Product
def update_product():
    print("\n--- Update Product ---")

    product_id = int(input("Enter product ID: "))

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if product:
        name = input("Enter new product name: ")
        category = input("Enter new category: ")
        quantity = int(input("Enter new quantity: "))
        price = float(input("Enter new price: "))

        if quantity < 0 or price < 0:
            print("Quantity and price cannot be negative.")
            return

        cursor.execute("""
        UPDATE products
        SET name = ?, category = ?, quantity = ?, price = ?
        WHERE id = ?
        """, (name, category, quantity, price, product_id))

        conn.commit()
        print("Product updated successfully!")
    else:
        print("Product not found.")


# Delete Product
def delete_product():
    print("\n--- Delete Product ---")

    product_id = int(input("Enter product ID: "))

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if product:
        cursor.execute(
            "DELETE FROM products WHERE id = ?",
            (product_id,)
        )

        conn.commit()
        print("Product deleted successfully!")
    else:
        print("Product not found.")


# Low Stock Products
def low_stock():
    print("\n--- Low Stock Products ---")

    cursor.execute(
        "SELECT * FROM products WHERE quantity < 10"
    )

    products = cursor.fetchall()

    if products:
        for product in products:
            print(product)
    else:
        print("No low-stock products.")


# Total Inventory Value
def inventory_value():
    cursor.execute("""
    SELECT SUM(quantity * price) FROM products
    """)

    result = cursor.fetchone()[0]

    print("\nTotal Inventory Value: Rs.", result or 0)


# Main Menu
while True:
    print("\n================================")
    print("  INVENTORY MANAGEMENT SYSTEM")
    print("================================")
    print("1. Add Product")
    print("2. View Products")
    print("3. Search Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Low Stock Products")
    print("7. Total Inventory Value")
    print("8. Exit")

    choice = input("\nEnter your choice: ")

    try:
        if choice == '1':
            add_product()

        elif choice == '2':
            view_products()

        elif choice == '3':
            search_product()

        elif choice == '4':
            update_product()

        elif choice == '5':
            delete_product()

        elif choice == '6':
            low_stock()

        elif choice == '7':
            inventory_value()

        elif choice == '8':
            print("Thank you for using Inventory Management System!")
            break

        else:
            print("Invalid choice. Please try again.")

    except ValueError:
        print("Please enter valid numeric values.")

    except sqlite3.Error as e:
        print("Database Error:", e)

conn.close()
