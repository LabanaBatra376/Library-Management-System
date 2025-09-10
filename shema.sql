-- Create the database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Table to store books
CREATE TABLE IF NOT EXISTS Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(50),
    available BOOLEAN DEFAULT TRUE
);

-- Table to store members (students)
CREATE TABLE IF NOT EXISTS Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

-- Table to store borrow/return records
CREATE TABLE IF NOT EXISTS BorrowRecords (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    book_id INT,
    borrow_date DATE,
    return_date DATE,
    status ENUM('Borrowed','Returned') DEFAULT 'Borrowed',
    FOREIGN KEY(student_id) REFERENCES Students(student_id),
    FOREIGN KEY(book_id) REFERENCES Books(book_id)
);

-- Insert sample books
INSERT INTO Books (title, author, genre) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic'),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction'),
('1984', 'George Orwell', 'Dystopian'),
('Python Crash Course', 'Eric Matthes', 'Programming'),
('Introduction to Algorithms', 'Thomas H. Cormen', 'Computer Science');

-- Insert sample members
INSERT INTO Students (name, department, email) VALUES
('Alice Johnson', 'Computer Science', 'alice@example.com'),
('Bob Smith', 'Electrical Engineering', 'bob@example.com'),
('Charlie Brown', 'Mechanical Engineering', 'charlie@example.com'),
('Diana Prince', 'Civil Engineering', 'diana@example.com');
