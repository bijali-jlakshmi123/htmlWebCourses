import tkinter as tk
from tkinter import ttk, messagebox

# Functions
def add_item():
    item = item_text.get()
    qty = qty_text.get()
    price = price_text.get()
    
    if item == "" or qty == "" or price == "":
        messagebox.showerror("Error", "Please fill all fields")
        return
    
    try:
        qty = int(qty)
        price = float(price)
    except ValueError:
        messagebox.showerror("Error", "Quantity and Price must be valid numbers")
        return
        
    total = qty * price
    total_text.config(state='normal')
    total_text.delete(0, tk.END)
    total_text.insert(0, str(total))
    total_text.config(state='readonly')
    
    # Add to Treeview
    bill_tree.insert("", tk.END, values=(item, qty, price, total))
    
    # Clear entry fields
    item_text.delete(0, tk.END)
    qty_text.delete(0, tk.END)
    price_text.delete(0, tk.END)

def generate_bill():
    bill_area.delete(1.0, tk.END)
    bill_area.insert(tk.END, "\t\tBilling Software\n")
    bill_area.insert(tk.END, "\t\t================\n\n")
    bill_area.insert(tk.END, f"{'Item Name':<20}\t{'Qty':<5}\t{'Price':<10}\t{'Total':<10}\n")
    bill_area.insert(tk.END, "-"*65 + "\n")
    
    grand_total = 0
    for child in bill_tree.get_children():
        item, qty, price, total = bill_tree.item(child)["values"]
        grand_total += float(total)
        bill_area.insert(tk.END, f"{str(item):<20}\t{str(qty):<5}\t{str(price):<10}\t{str(total):<10}\n")
        
    bill_area.insert(tk.END, "-"*65 + "\n")
    bill_area.insert(tk.END, f"Grand Total:\t\t\t\t\t{grand_total}\n")
    
def clear_all():
    item_text.delete(0, tk.END)
    qty_text.delete(0, tk.END)
    price_text.delete(0, tk.END)
    total_text.config(state='normal')
    total_text.delete(0, tk.END)
    total_text.config(state='readonly')
    
    for item in bill_tree.get_children():
        bill_tree.delete(item)
    
    bill_area.delete(1.0, tk.END)

window=tk.Tk()
window.title("Billing System")
window.geometry("900x600")

# Heading
heading = tk.Label(
    window,
    text="Billing Software",
    font=("Arial", 30, "bold"),
    fg="white",
    bg="#1a1a1a"
)
heading.pack(fill=tk.X, pady=10)

# Input Frame
item_details=tk.Frame(window)
item_details.pack(pady=10)
for col in range(4):
    item_details.columnconfigure(col,minsize=180)

tk.Label(item_details,text="Item Name", font=("Arial",15)).grid(row=0,column=0)
tk.Label(item_details,text="Quantity", font=("Arial",15)).grid(row=0,column=1)
tk.Label(item_details,text="Price", font=("Arial",15)).grid(row=0,column=2)
tk.Label(item_details,text="Total", font=("Arial",15)).grid(row=0,column=3)

item_text=tk.Entry(item_details, font=("Arial",15), width=15)
item_text.grid(row=1,column=0, padx=5)
qty_text=tk.Entry(item_details, font=("Arial",15), width=15)
qty_text.grid(row=1,column=1, padx=5)
price_text=tk.Entry(item_details, font=("Arial",15), width=15)
price_text.grid(row=1,column=2, padx=5)
total_text=tk.Entry(item_details, font=("Arial",15), width=15, state='readonly')
total_text.grid(row=1,column=3, padx=5)

# Buttons Frame
btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Item", font=("Arial", 12), bg="green", fg="white", width=15, command=add_item).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Generate Bill", font=("Arial", 12), bg="blue", fg="white", width=15, command=generate_bill).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Clear", font=("Arial", 12), bg="red", fg="white", width=15, command=clear_all).grid(row=0, column=2, padx=10)

# Treeview & Bill Area Frame
bottom_frame = tk.Frame(window)
bottom_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Treeview for Items
columns = ("Item Name", "Quantity", "Price", "Total")
bill_tree = ttk.Treeview(bottom_frame, columns=columns, show="headings", height=8)
for col in columns:
    bill_tree.heading(col, text=col)
    bill_tree.column(col, width=120)
bill_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for Treeview
tree_scroll = ttk.Scrollbar(bottom_frame, orient="vertical", command=bill_tree.yview)
tree_scroll.pack(side=tk.LEFT, fill=tk.Y)
bill_tree.configure(yscrollcommand=tree_scroll.set)

# Text Area for Bill Receipt
bill_area = tk.Text(bottom_frame, font=("Courier", 10), width=50)
bill_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10,0))

window.mainloop()