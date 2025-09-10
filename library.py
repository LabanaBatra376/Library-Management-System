import mysql.connector
from datetime import date, timedelta

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
    title = input("Enter book title: ")
    author = input("Enter author: ")
    genre = input("Enter genre: ")

    query = "INSERT INTO Books (title, author, genre) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, author, genre))
    db.commit()
    print("✅ Book added successfully!")

def add_member():
    name = input("Enter member name: ")
    dept = input("Enter department: ")
    email = input("Enter email: ")

    query = "INSERT INTO Students (name, department, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, dept, email))
    db.commit()
    print("✅ Member added successfully!")

def borrow_book():
    student_id = int(input("Enter student ID: "))
    book_id = int(input("Enter book ID: "))

    cursor.execute("SELECT available FROM Books WHERE book_id=%s", (book_id,))
    book = cursor.fetchone()

    if book and book[0]:
        borrow_date = date.today()
        return_date = borrow_date + timedelta(days=14)  # 2 weeks
        query = "INSERT INTO BorrowRecords (student_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (student_id, book_id, borrow_date, return_date))
        cursor.execute("UPDATE Books SET available=FALSE WHERE book_id=%s", (book_id,))
        db.commit()
        print("✅ Book borrowed successfully! Due on", return_date)
    else:
        print("❌ Book not available.")

def return_book():
    record_id = int(input("Enter borrow record ID: "))

    cursor.execute("SELECT book_id FROM BorrowRecords WHERE record_id=%s AND status='Borrowed'", (record_id,))
    record = cursor.fetchone()

    if record:
        book_id = record[0]
        cursor.execute("UPDATE BorrowRecords SET status='Returned' WHERE record_id=%s", (record_id,))
        cursor.execute("UPDATE Books SET available=TRUE WHERE book_id=%s", (book_id,))
        db.commit()
        print("✅ Book returned successfully!")
    else:
        print("❌ Invalid record or already returned.")

def view_borrowed_books():
    cursor.execute("""
        SELECT r.record_id, s.name, b.title, r.borrow_date, r.return_date
        FROM BorrowRecords r
        JOIN Students s ON r.student_id=s.student_id
        JOIN Books b ON r.book_id=b.book_id
        WHERE r.status='Borrowed'
    """)
    records = cursor.fetchall()
    if records:
        print("\n--- Borrowed Books ---")
        for row in records:
            print(f"RecordID: {row[0]} | Student: {row[1]} | Book: {row[2]} | Borrowed: {row[3]} | Due: {row[4]}")
    else:
        print("No borrowed books.")

def search_books():
    keyword = input("Enter keyword (title/author/genre): ")
    query = "SELECT * FROM Books WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    if results:
        print("\n--- Search Results ---")
        for row in results:
            print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Genre: {row[3]} | Available: {row[4]}")
    else:
        print("No books found.")

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
    if overdue:
        print("\n--- Overdue Books ---")
        for row in overdue:
            print(f"RecordID: {row[0]} | Student: {row[1]} | Book: {row[2]} | Due: {row[3]}")
    else:
        print("No overdue books.")

def count_borrowed_books():
    query = """
        SELECT s.name, COUNT(r.record_id) AS borrowed_count
        FROM Students s
        LEFT JOIN BorrowRecords r ON s.student_id=r.student_id AND r.status='Borrowed'
        GROUP BY s.student_id
    """
    cursor.execute(query)
    counts = cursor.fetchall()
    print("\n--- Borrowed Books per Member ---")
    for row in counts:
        print(f"Student: {row[0]} | Borrowed Books: {row[1]}")


def show_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    if books:
        print("\n--- All Books ---")
        for row in books:
            print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Genre: {row[3]} | Available: {row[4]}")
    else:
        print("No books available.")

def show_books_id():
    cursor.execute("SELECT book_id, title FROM Books")
    books = cursor.fetchall()
    if books:
        print("\n--- Book IDs ---")
        for row in books:
            print(f"BookID: {row[0]} | Title: {row[1]}")
    else:
        print("No books available.")


# ------------------ Menu Loop ------------------
while True:
    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Borrowed Books")
    print("6. Search Books")
    print("7. List Overdue Books")
    print("8. Count Borrowed Books per Member")
    print("9. Show All Books")
    print("10. Show Book IDs")
    print("11. Exit")


    choice = input("Enter choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        add_member()
    elif choice == "3":
        borrow_book()
    elif choice == "4":
        return_book()
    elif choice == "5":
        view_borrowed_books()
    elif choice == "6":
        search_books()
    elif choice == "7":
        list_overdue_books()
    elif choice == "8":
        count_borrowed_books()
    elif choice=="9":
        show_books()
    elif choice=="10":
        show_books_id()
    elif choice == "11":
        print("👋 Exiting... Goodbye!")
        break
    else:
        print("❌ Invalid choice, try again.")
