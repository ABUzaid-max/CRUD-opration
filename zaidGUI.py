import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["LibraryDB"]
collection = db["books"]

# Window
root = tk.Tk()
root.title("Library Manager - Abuzaid Shaikh")
root.geometry("650x450")

# Title
title = tk.Label(root, text="510 - Abuzaid Shaikh | Library Book Manager (MongoDB + Tkinter)", 
                 font=("Helvetica", 15, "bold"), fg="darkgreen")
title.pack(pady=15)

# Frame for form
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Labels & Entry fields
tk.Label(form_frame, text="Book ID:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
book_id_entry = tk.Entry(form_frame, width=35)
book_id_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Title:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
title_entry = tk.Entry(form_frame, width=35)
title_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Author:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
author_entry = tk.Entry(form_frame, width=35)
author_entry.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Genre:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
genre_entry = tk.Entry(form_frame, width=35)
genre_entry.grid(row=3, column=1, pady=5)

# ---------------- Insert ----------------
def insert():
    book_id = book_id_entry.get().strip()
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()

    if not (book_id and title and author and genre):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    try:
        collection.insert_one({"book_id": book_id, "title": title, "author": author, "genre": genre})
        messagebox.showinfo("Success", "Book added successfully!")
        book_id_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        genre_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Insert failed: {e}")

# ---------------- Read ----------------
def read():
    try:
        documents = collection.find()
        result_text.delete(1.0, tk.END)
        for doc in documents:
            result_text.insert(tk.END, f"ID: {doc['book_id']}, Title: {doc['title']}, Author: {doc['author']}, Genre: {doc['genre']}\n")
    except:
        messagebox.showerror("Error", "Failed to fetch records")

# ---------------- Update ----------------
def update():
    win = Toplevel(root)
    win.title("Update Book")
    win.geometry("400x250")

    tk.Label(win, text="Enter Title to Update:").pack(pady=5)
    old_title_entry = tk.Entry(win, width=30)
    old_title_entry.pack()

    tk.Label(win, text="New Author:").pack(pady=5)
    new_author_entry = tk.Entry(win, width=30)
    new_author_entry.pack()

    tk.Label(win, text="New Genre:").pack(pady=5)
    new_genre_entry = tk.Entry(win, width=30)
    new_genre_entry.pack()

    def confirm_update():
        old_title = old_title_entry.get().strip()
        new_author = new_author_entry.get().strip()
        new_genre = new_genre_entry.get().strip()

        if not (old_title and new_author and new_genre):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        result = collection.update_one({"title": old_title}, {"$set": {"author": new_author, "genre": new_genre}})
        if result.modified_count > 0:
            messagebox.showinfo("Success", "Book updated successfully!")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No matching book found.")

    tk.Button(win, text="Update Now", command=confirm_update).pack(pady=15)

# ---------------- Delete ----------------
def delete():
    win = Toplevel(root)
    win.title("Delete Book")
    win.geometry("300x200")

    tk.Label(win, text="Enter Book ID to Delete:").pack(pady=10)
    del_id_entry = tk.Entry(win, width=30)
    del_id_entry.pack()

    def confirm_delete():
        del_id = del_id_entry.get().strip()
        if not del_id:
            messagebox.showwarning("Warning", "Book ID is required!")
            return

        result = collection.delete_one({"book_id": del_id})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Book deleted successfully!")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No book found with given ID.")

    tk.Button(win, text="Delete Now", command=confirm_delete).pack(pady=15)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Insert", command=insert, width=12, bg="lightgreen").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Show Books", command=read, width=12, bg="lightblue").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Update", command=update, width=12, bg="orange").grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Delete", command=delete, width=12, bg="red").grid(row=0, column=3, padx=10)

# Result Text Area
result_text = scrolledtext.ScrolledText(root, width=75, height=8)
result_text.pack(pady=10)

root.mainloop()
