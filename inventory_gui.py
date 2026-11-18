
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE ----------------

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

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

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("StockPro | Inventory Management")
root.geometry("1250x760")
root.minsize(1000, 650)
root.configure(bg="#F3F5FA")

BG = "#F3F5FA"
WHITE = "#FFFFFF"
NAVY = "#172554"
BLUE = "#4F46E5"
GREEN = "#059669"
RED = "#DC2626"
TEXT = "#1E293B"
MUTED = "#64748B"

selected_id = None

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=35,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#E8ECF5",
    foreground=NAVY,
    font=("Arial", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#C7D2FE")],
    foreground=[("selected", NAVY)]
)

style.configure(
    "TCombobox",
    padding=8,
    font=("Arial", 11)
)

# ---------------- FUNCTIONS ----------------

def get_products():
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    return cursor.fetchall()


def clear_form():
    global selected_id
    selected_id = None

    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

    product_search.set("")


def refresh_search_dropdown():
    products = get_products()

    product_names = sorted(set(
        row[1] for row in products
    ), key=str.lower)

    product_search["values"] = product_names


def update_dashboard():
    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(quantity), 0),
        COALESCE(SUM(quantity * price), 0)
        FROM products
    """)

    total, stock, value = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*) FROM products
        WHERE quantity < 10
    """)

    low = cursor.fetchone()[0]

    total_value_label.config(text=f"{total}")
    stock_value_label.config(text=f"{stock}")
    low_value_label.config(text=f"{low}")
    value_value_label.config(text=f"₹{value:,.2f}")


def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    for row in get_products():
        tree.insert(
            "",
            tk.END,
            values=row,
            tags=("low",) if row[3] < 10 else ("normal",)
        )

    tree.tag_configure("low", foreground=RED)
    tree.tag_configure("normal", foreground=TEXT)

    update_dashboard()
    refresh_search_dropdown()


def validate_form():
    name = name_entry.get().strip()
    category = category_entry.get().strip()

    if not name or not category:
        messagebox.showerror(
            "Missing Details",
            "Please enter product name and category."
        )
        return None

    try:
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())

        if quantity < 0 or price < 0:
            raise ValueError

        return name, category, quantity, price

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Quantity must be a non-negative integer and price must be non-negative."
        )
        return None


def add_product():
    data = validate_form()

    if data is None:
        return

    cursor.execute("""
        INSERT INTO products (name, category, quantity, price)
        VALUES (?, ?, ?, ?)
    """, data)

    conn.commit()

    refresh_table()
    clear_form()

    messagebox.showinfo(
        "Success",
        "New product added successfully!"
    )


def update_product():
    if selected_id is None:
        messagebox.showwarning(
            "Select Product",
            "Please select a product from the table or search dropdown."
        )
        return

    data = validate_form()

    if data is None:
        return

    cursor.execute("""
        UPDATE products
        SET name=?, category=?, quantity=?, price=?
        WHERE id=?
    """, (*data, selected_id))

    conn.commit()

    refresh_table()
    clear_form()

    messagebox.showinfo(
        "Updated",
        "Product details updated successfully!"
    )


def delete_product():
    if selected_id is None:
        messagebox.showwarning(
            "Select Product",
            "Please select a product first."
        )
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this product?"
    )

    if answer:
        cursor.execute(
            "DELETE FROM products WHERE id=?",
            (selected_id,)
        )

        conn.commit()
        refresh_table()
        clear_form()

        messagebox.showinfo(
            "Deleted",
            "Product deleted successfully!"
        )


def load_product(row):
    global selected_id

    selected_id = row[0]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, row[1])

    category_entry.delete(0, tk.END)
    category_entry.insert(0, row[2])

    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, row[3])

    price_entry.delete(0, tk.END)
    price_entry.insert(0, row[4])

    product_search.set(row[1])


def select_from_dropdown(event=None):
    name = product_search.get().strip()

    if not name:
        return

    cursor.execute(
        "SELECT * FROM products WHERE name=? ORDER BY id DESC",
        (name,)
    )

    row = cursor.fetchone()

    if row:
        load_product(row)

        for item in tree.get_children():
            values = tree.item(item, "values")
            if int(values[0]) == row[0]:
                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)
                break


def filter_products(event=None):
    typed = product_search.get().strip().lower()

    cursor.execute("SELECT DISTINCT name FROM products")
    all_names = [row[0] for row in cursor.fetchall()]

    matches = [
        name for name in all_names
        if typed in name.lower()
    ]

    product_search["values"] = matches

    # Display matching product suggestions
    if matches and typed:
        product_search.event_generate("<Down>")


def search_products():
    keyword = product_search.get().strip()

    if not keyword:
        refresh_table()
        return

    cursor.execute("""
        SELECT * FROM products
        WHERE name LIKE ? OR category LIKE ?
        ORDER BY id DESC
    """, (f"%{keyword}%", f"%{keyword}%"))

    results = cursor.fetchall()

    for item in tree.get_children():
        tree.delete(item)

    for row in results:
        tree.insert(
            "",
            tk.END,
            values=row,
            tags=("low",) if row[3] < 10 else ("normal",)
        )

    tree.tag_configure("low", foreground=RED)
    tree.tag_configure("normal", foreground=TEXT)

    if not results:
        messagebox.showinfo(
            "Search",
            "No matching products found."
        )


def select_from_table(event):
    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")

        cursor.execute(
            "SELECT * FROM products WHERE id=?",
            (values[0],)
        )

        row = cursor.fetchone()

        if row:
            load_product(row)


def show_all_products():
    clear_form()
    refresh_table()


# ---------------- HEADER ----------------

header = tk.Frame(root, bg=NAVY, height=85)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="📦  STOCKPRO",
    font=("Arial", 23, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(side="left", padx=30, pady=20)

tk.Label(
    header,
    text="INVENTORY MANAGEMENT SYSTEM",
    font=("Arial", 11, "bold"),
    bg=NAVY,
    fg="#C7D2FE"
).pack(side="right", padx=30)


# ---------------- SIDEBAR ----------------

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True)

sidebar = tk.Frame(main, bg="#1E293B", width=205)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="MAIN MENU",
    bg="#1E293B",
    fg="#94A3B8",
    font=("Arial", 10, "bold")
).pack(anchor="w", padx=22, pady=(30, 15))


def menu_button(text, command):
    tk.Button(
        sidebar,
        text=text,
        command=command,
        bg="#1E293B",
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        font=("Arial", 11, "bold"),
        padx=22,
        pady=14,
        cursor="hand2"
    ).pack(fill="x", padx=8, pady=3)


menu_button("▦  Dashboard", show_all_products)
menu_button("＋  Add Product", clear_form)
menu_button("⌕  Search Products", lambda: product_search.focus_set())
menu_button("↻  Refresh", refresh_table)

tk.Label(
    sidebar,
    text="StockPro v2.0",
    bg="#1E293B",
    fg="#94A3B8",
    font=("Arial", 9)
).pack(side="bottom", pady=20)


# ---------------- CONTENT ----------------

content = tk.Frame(main, bg=BG)
content.pack(side="left", fill="both", expand=True, padx=25, pady=20)

tk.Label(
    content,
    text="Dashboard Overview",
    font=("Arial", 23, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    content,
    text="Manage your products and monitor your stock.",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 18))


# ---------------- DASHBOARD CARDS ----------------

cards = tk.Frame(content, bg=BG)
cards.pack(fill="x", pady=5)

def create_card(parent, heading, color):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    card.pack(side="left", fill="both", expand=True, padx=(0, 12))

    tk.Label(
        card,
        text=heading,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w", padx=15, pady=(15, 5))

    value = tk.Label(
        card,
        text="0",
        font=("Arial", 23, "bold"),
        bg=WHITE,
        fg=color
    )

    value.pack(anchor="w", padx=15, pady=(0, 15))

    return value


total_value_label = create_card(
    cards, "TOTAL PRODUCTS", BLUE
)

stock_value_label = create_card(
    cards, "TOTAL STOCK", GREEN
)

low_value_label = create_card(
    cards, "LOW STOCK ITEMS", RED
)

value_value_label = create_card(
    cards, "INVENTORY VALUE", "#D97706"
)


# ---------------- PRODUCT FORM ----------------

form = tk.LabelFrame(
    content,
    text="  Product Information  ",
    bg=WHITE,
    fg=NAVY,
    font=("Arial", 12, "bold"),
    padx=15,
    pady=12
)

form.pack(fill="x", pady=18)

labels = [
    "Product Name",
    "Category",
    "Quantity",
    "Price (₹)"
]

for i, label in enumerate(labels):
    tk.Label(
        form,
        text=label,
        bg=WHITE,
        fg=TEXT,
        font=("Arial", 10, "bold")
    ).grid(row=0, column=i, padx=10, pady=5, sticky="w")

name_entry = tk.Entry(form, width=22, font=("Arial", 11))
category_entry = tk.Entry(form, width=19, font=("Arial", 11))
quantity_entry = tk.Entry(form, width=13, font=("Arial", 11))
price_entry = tk.Entry(form, width=13, font=("Arial", 11))

name_entry.grid(row=1, column=0, padx=10, pady=8)
category_entry.grid(row=1, column=1, padx=10, pady=8)
quantity_entry.grid(row=1, column=2, padx=10, pady=8)
price_entry.grid(row=1, column=3, padx=10, pady=8)


# ---------------- ACTION BUTTONS ----------------

actions = tk.Frame(form, bg=WHITE)
actions.grid(row=2, column=0, columnspan=4, pady=12)

def action_button(parent, text, command, color):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        font=("Arial", 10, "bold"),
        padx=16,
        pady=9,
        cursor="hand2"
    )


action_button(
    actions, "＋ Add Product", add_product, BLUE
).pack(side="left", padx=5)

action_button(
    actions, "✎ Update", update_product, GREEN
).pack(side="left", padx=5)

action_button(
    actions, "✕ Delete", delete_product, RED
).pack(side="left", padx=5)

action_button(
    actions, "Clear", clear_form, MUTED
).pack(side="left", padx=5)


# ---------------- INTERACTIVE SEARCH ----------------

search_frame = tk.LabelFrame(
    content,
    text="  Search Available Products  ",
    bg=WHITE,
    fg=NAVY,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=12
)

search_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    search_frame,
    text="Select or type product name:",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10)
).pack(side="left", padx=5)

product_search = ttk.Combobox(
    search_frame,
    width=35,
    font=("Arial", 11)
)

product_search.pack(side="left", padx=10)

product_search.bind(
    "<KeyRelease>", filter_products
)

product_search.bind(
    "<<ComboboxSelected>>",
    select_from_dropdown
)

action_button(
    search_frame, "Search", search_products, BLUE
).pack(side="left", padx=5)

action_button(
    search_frame, "Show All", show_all_products, MUTED
).pack(side="left", padx=5)


# ---------------- PRODUCT TABLE ----------------

table_box = tk.Frame(content, bg=WHITE)
table_box.pack(fill="both", expand=True)

tk.Label(
    table_box,
    text="Product Inventory",
    bg=WHITE,
    fg=NAVY,
    font=("Arial", 13, "bold")
).pack(anchor="w", padx=15, pady=12)

table_frame = tk.Frame(table_box, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

columns = (
    "ID", "Product Name", "Category",
    "Quantity", "Price (₹)"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

widths = [60, 190, 160, 110, 130]

for col, width in zip(columns, widths):
    tree.heading(col, text=col)
    tree.column(col, width=width, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tree.bind(
    "<<TreeviewSelect>>",
    select_from_table
)


# ---------------- START APPLICATION ----------------

refresh_table()

root.mainloop()

conn.close()
