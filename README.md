# StockPro Inventory Management System

A desktop and command-line inventory management project built with Python and SQLite. StockPro allows a small business or individual to maintain product records, monitor available stock, identify low-stock items, search inventory, and calculate the total value of all products.

The project includes two interfaces that use the same SQLite database:

- **Graphical interface:** `inventory_gui.py` provides an interactive Tkinter dashboard.
- **Command-line interface:** `inventory.py` provides a menu-based terminal experience.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Structure](#database-structure)
- [How the Project Works](#how-the-project-works)
- [Installation and Setup](#installation-and-setup)
- [Running the GUI](#running-the-gui)
- [Running the CLI](#running-the-cli)
- [Using the Application](#using-the-application)
- [Example Workflow](#example-workflow)
- [Low-Stock and Inventory Calculations](#low-stock-and-inventory-calculations)
- [Input and Validation Rules](#input-and-validation-rules)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

## Project Overview

Inventory management is the process of recording and controlling products held for sale or use. This project stores each product's name, category, quantity, and unit price in a local SQLite database.

StockPro demonstrates several common programming concepts:

- CRUD operations: Create, Read, Update, and Delete
- SQL database creation and queries
- Parameterized SQLite queries
- Python functions and menu-driven programs
- Input validation and error handling
- Tkinter graphical interface development
- Dashboard-style calculations
- Search and filtering
- Persistent local data storage

The database is stored in `inventory.db`, so products remain available after the application is closed and reopened.

## Features

### Shared Features

- Add a new product
- View all products
- Search for products
- Update product details
- Delete a product
- Track quantity and price
- Prevent negative quantities and prices
- Identify low-stock products
- Calculate total inventory value

### GUI Features

- Modern dashboard layout
- Product information form
- Interactive product table
- Product-name suggestions and filtering
- Dashboard cards for:
  - Total number of products
  - Total quantity in stock
  - Number of low-stock items
  - Total inventory value
- Low-stock rows highlighted in red
- Confirmation dialog before deleting
- Success and error message dialogs
- Sidebar navigation and refresh controls

### CLI Features

- Numbered terminal menu
- Formatted product table
- Partial name search
- Low-stock listing
- Numeric input validation
- SQLite error handling

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3 |
| Database | SQLite 3 |
| GUI framework | Tkinter |
| Additional GUI components | Tkinter `ttk` widgets |
| Currency display | Indian Rupees (`₹`) |

No third-party Python package is required. SQLite is included with Python, and Tkinter is included with most standard Python installations on Windows.

## Project Structure

```text
SQL project/
├── inventory.py       # Menu-based command-line application
├── inventory_gui.py   # Tkinter graphical interface
├── inventory.db       # SQLite database containing product records
└── README.md          # Project documentation
```

## Database Structure

Both interfaces connect to `inventory.db` and create the following table when it does not already exist.

### `products` Table

| Column | SQLite type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Unique product identifier |
| `name` | `TEXT NOT NULL` | Product name |
| `category` | `TEXT NOT NULL` | Product category |
| `quantity` | `INTEGER NOT NULL` | Quantity currently in stock |
| `price` | `REAL NOT NULL` | Unit price |

The database schema is created automatically:

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
```

The table uses an automatically increasing integer ID, making it easy to uniquely identify, update, and delete a product.

## How the Project Works

### GUI Workflow

1. `inventory_gui.py` opens a connection to `inventory.db`.
2. It creates the `products` table if it does not exist.
3. The dashboard queries the database and calculates summary values.
4. Product records are displayed in a `ttk.Treeview` table.
5. Selecting a row loads that product into the form.
6. Add, Update, and Delete actions execute parameterized SQL statements.
7. The table and dashboard refresh after each data change.

### CLI Workflow

1. `inventory.py` opens a connection to `inventory.db`.
2. It creates the `products` table if needed.
3. A numbered menu repeatedly accepts the user's choice.
4. Each menu option calls a dedicated Python function.
5. SQL results are displayed in the terminal.
6. The connection is closed when the user chooses **Exit**.

## Installation and Setup

### 1. Install Python

Install Python 3 on your computer and ensure that `python` is available from Command Prompt or PowerShell.

Check the installation:

```powershell
python --version
```

### 2. Open the Project Folder

Change to the project directory:

```powershell
cd "C:\Users\ASUS\SQL project"
```

It is important to run the scripts from the project folder because both Python files open `inventory.db` using a relative file name.

### 3. Verify Tkinter

Tkinter is usually distributed with Python on Windows. Verify it with:

```powershell
python -c "import tkinter"
```

If no error appears, Tkinter is available.

## Running the GUI

From the project folder, run:

```powershell
python inventory_gui.py
```

The StockPro dashboard window will open.

## Running the CLI

From the project folder, run:

```powershell
python inventory.py
```

The terminal will display:

```text
================================
  INVENTORY MANAGEMENT SYSTEM
================================
1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Low Stock Products
7. Total Inventory Value
8. Exit
```

Enter a number between `1` and `8` to choose an action.

## Using the Application

### Add a Product

Enter:

- Product name
- Category
- Quantity
- Unit price

The quantity must be a whole number. The price may include decimal values.

Example:

```text
Product name: Laptop
Category: Accessories
Quantity: 25
Price: 135000
```

### Search for a Product

In the GUI, type or select a name and press **Search**. The GUI searches both product names and categories, while the CLI searches product names with a partial match.

Example search:

```text
lap
```

This may match `Laptop`, `Laptop Stand`, or any name containing `lap`.

### Update a Product

GUI:

1. Select a row in the table or a name in the search box.
2. Edit the fields.
3. Click **Update**.

CLI:

1. Enter the product ID.
2. Enter the replacement name, category, quantity, and price.

### Delete a Product

GUI:

1. Select a product.
2. Click **Delete**.
3. Confirm the deletion in the dialog.

CLI:

1. Enter the product ID.
2. The application reports whether the product was found and deleted.

### Clear the GUI Form

Click **Clear** or use **Add Product** in the sidebar to clear the form and return to add mode.

### Refresh or Show All

- **Refresh** reloads the table and dashboard totals.
- **Show All** clears the form and removes an active search filter.
- **Dashboard** also restores the complete product list.

## Example Workflow

Suppose the inventory contains these products:

| ID | Name | Category | Quantity | Price |
|---|---|---|---:|---:|
| 1 | Laptop | Accessories | 25 | ₹135,000 |
| 2 | Fridge | Appliances | 7 | ₹45,000 |

After adding these records:

- Total products = `2`
- Total stock = `32`
- Low-stock items = `1`
- Inventory value = `(25 × 135000) + (7 × 45000)`
- Inventory value = `₹3,690,000`

## Low-Stock and Inventory Calculations

### Low-Stock Rule

Stock is considered low when:

```text
quantity < 10
```

The GUI shows these rows in red and counts them in the **LOW STOCK ITEMS** dashboard card.

The CLI's **Low Stock Products** option retrieves the same quantity-based rule.

### Inventory Value Formula

For every product:

```text
Product value = quantity × unit price
```

The complete inventory value is the sum of all product values:

```sql
SELECT SUM(quantity * price) FROM products;
```

If the table has no products, the application displays `0` instead of a null or missing value.

## Input and Validation Rules

The application applies the following rules:

- Product name cannot be blank.
- Category cannot be blank.
- Quantity must be a non-negative integer.
- Price must be non-negative.
- A product must exist before it can be updated or deleted.
- Numeric conversion errors are handled without crashing the menu.
- The GUI displays clear validation dialogs.
- SQL values are passed through parameters instead of being concatenated into SQL text.

## Troubleshooting

### The GUI window does not open

- Confirm that Python is installed.
- Run the script from Command Prompt or PowerShell.
- Check whether Tkinter is available with `python -c "import tkinter"`.

### Tkinter is missing

Reinstall or repair Python and enable the Tkinter/Tcl option. On some Windows installations, Tkinter is included with the standard installer.

### The wrong database is being used

Both scripts open `inventory.db` relative to the current working directory. Run them from the project directory to use the same database.

### `ValueError` or invalid input

Enter a whole number for quantity and a numeric value for price. Do not enter negative values.

### SQLite database locked

Close duplicate instances of the application and run one instance at a time. SQLite locking can also occur when a database viewer has the file open exclusively.

### Product search returns no results

Try a shorter or partial product name. The GUI search can also match categories.

## Limitations

- The database is local and does not synchronize across devices.
- The project has no login or role-based permissions.
- Product names are not required to be unique.
- The low-stock threshold is fixed at fewer than 10 units.
- The CLI and GUI are separate processes and should not be run simultaneously while modifying data.
- The GUI has no built-in backup or export feature.
- The project is intended for learning and small local inventories rather than enterprise inventory control.

## Future Improvements

Possible enhancements include:

- Add supplier information
- Add stock movement history
- Allow customizable low-stock thresholds
- Add category filtering
- Export inventory reports to CSV or PDF
- Add database backups
- Add product images
- Add user authentication
- Use a class-based or layered code structure
- Add unit tests
- Package the GUI as a Windows executable

## License

This project is provided for educational and personal inventory management use unless a different license is added to the repository.
