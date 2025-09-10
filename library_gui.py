import mysql.connector
from datetime import date, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# ------------------ Database Connection ------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="labana123*",   # <-- change this
    database="library_db"      # <-- make sure database exists
)
cursor = db.cursor()

# ------------------ Functions ------------------

def add_book():
    title = simpledialog.askstring("Add Book", "Enter book title:")
    author = simpledialog.askstring("Add Book", "Enter author:")
    genre = simpledialog.askstring("Add Book", "Enter genre:")

    if title and author and genre:
        query = "INSERT INTO Books (title, author, genre) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, author, genre))
        db.commit()
        messagebox.showinfo("Success", "✅ Book added successfully!")

def add_member():
    name = simpledialog.askstring("Add Member", "Enter member name:")
    dept = simpledialog.askstring("Add Member", "Enter department:")
    email = simpledialog.askstring("Add Member", "Enter email:")

    if name and dept and email:
        query = "INSERT INTO Students (name, department, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, dept, email))
        db.commit()
        messagebox.showinfo("Success", "✅ Member added successfully!")

def borrow_book():
    student_id = simpledialog.askinteger("Borrow Book", "Enter student ID:")
    book_id = simpledialog.askinteger("Borrow Book", "Enter book ID:")

    cursor.execute("SELECT available FROM Books WHERE book_id=%s", (book_id,))
    book = cursor.fetchone()

    if book and book[0]:
        borrow_date = date.today()
        return_date = borrow_date + timedelta(days=14)
        query = "INSERT INTO BorrowRecords (student_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (student_id, book_id, borrow_date, return_date))
        cursor.execute("UPDATE Books SET available=FALSE WHERE book_id=%s", (book_id,))
        db.commit()
        messagebox.showinfo("Success", f"✅ Book borrowed! Due on {return_date}")
    else:
        messagebox.showerror("Error", "❌ Book not available.")

def return_book():
    record_id = simpledialog.askinteger("Return Book", "Enter borrow record ID:")

    cursor.execute("SELECT book_id FROM BorrowRecords WHERE record_id=%s AND status='Borrowed'", (record_id,))
    record = cursor.fetchone()

    if record:
        book_id = record[0]
        cursor.execute("UPDATE BorrowRecords SET status='Returned' WHERE record_id=%s", (record_id,))
        cursor.execute("UPDATE Books SET available=TRUE WHERE book_id=%s", (book_id,))
        db.commit()
        messagebox.showinfo("Success", "✅ Book returned successfully!")
    else:
        messagebox.showerror("Error", "❌ Invalid record or already returned.")

def view_borrowed_books():
    cursor.execute("""
        SELECT r.record_id, s.name, b.title, r.borrow_date, r.return_date
        FROM BorrowRecords r
        JOIN Students s ON r.student_id=s.student_id
        JOIN Books b ON r.book_id=b.book_id
        WHERE r.status='Borrowed'
    """)
    records = cursor.fetchall()
    output = "\n".join([f"RecordID: {r[0]} | Student: {r[1]} | Book: {r[2]} | Borrowed: {r[3]} | Due: {r[4]}" for r in records])
    messagebox.showinfo("Borrowed Books", output if output else "No borrowed books.")

def search_books():
    keyword = simpledialog.askstring("Search Books", "Enter keyword (title/author/genre):")
    query = "SELECT * FROM Books WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    output = "\n".join([f"ID: {r[0]} | Title: {r[1]} | Author: {r[2]} | Genre: {r[3]} | Available: {r[4]}" for r in results])
    messagebox.showinfo("Search Results", output if output else "No books found.")

def list_overdue_books():
    today = date.today()
    query = """
        SELECT r.record_id, s.name, b.title, r.return_date
        FROM BorrowRecords r
        JOIN Students s ON r.student_id=s.student_id
        JOIN Books b ON r.book_id=b.book_id
        WHERE r.status='Borrowed' AND r.return_date < %s
    """
    cursor.execute(query, (today,))
    overdue = cursor.fetchall()
    output = "\n".join([f"RecordID: {r[0]} | Student: {r[1]} | Book: {r[2]} | Due: {r[3]}" for r in overdue])
    messagebox.showinfo("Overdue Books", output if output else "No overdue books.")

def count_borrowed_books():
    query = """
        SELECT s.name, COUNT(r.record_id) AS borrowed_count
        FROM Students s
        LEFT JOIN BorrowRecords r ON s.student_id=r.student_id AND r.status='Borrowed'
        GROUP BY s.student_id
    """
    cursor.execute(query)
    counts = cursor.fetchall()
    output = "\n".join([f"Student: {r[0]} | Borrowed Books: {r[1]}" for r in counts])
    messagebox.showinfo("Borrowed Books per Member", output if output else "No data.")

def show_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    output = "\n".join([f"ID: {b[0]} | Title: {b[1]} | Author: {b[2]} | Genre: {b[3]} | Available: {b[4]}" for b in books])
    messagebox.showinfo("All Books", output if output else "No books available.")

def show_books_id():
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    output = "\n".join([f"BookID: {b[0]} | Title: {b[1]}" for b in books])
    messagebox.showinfo("Book IDs", output if output else "No books available.")

# ------------------ GUI ------------------
root = tk.Tk()
root.title("📚 Library Management System")
root.geometry("400x500")

tk.Label(root, text="Library Management System", font=("Arial", 16, "bold")).pack(pady=10)

buttons = [
    ("Add Book", add_book),
    ("Add Member", add_member),
    ("Borrow Book", borrow_book),
    ("Return Book", return_book),
    ("View Borrowed Books", view_borrowed_books),
    ("Search Books", search_books),
    ("List Overdue Books", list_overdue_books),
    ("Count Borrowed Books per Member", count_borrowed_books),
    ("Show All Books", show_books),
    ("Show Book IDs", show_books_id),
    ("Exit", root.quit)
]

for text, cmd in buttons:
    tk.Button(root, text=text, width=30, command=cmd).pack(pady=5)

root.mainloop()
