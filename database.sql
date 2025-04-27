- Create Database
CREATE DATABASE libraryDB;
USE libraryDB;

-- Admin Table
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Books Table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(100),
    is_borrowed BOOLEAN DEFAULT FALSE
);

-- Borrow Table
CREATE TABLE borrow (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

ALTER TABLE borrow ADD COLUMN returned BOOLEAN DEFAULT FALSE;

INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

-- Insert Sample Users
INSERT INTO users (username, password) VALUES
('alice', 'password1'),
('bob', 'password2'),
('charlie', 'password3');

-- Insert Sample Books
INSERT INTO books (title, author, isbn, category, is_borrowed) VALUES
('The Hobbit', 'J.R.R. Tolkien', '9780345339683', 'Fantasy', FALSE),
('The Alchemist', 'Paulo Coelho', '9780061122415', 'Philosophy', FALSE),
('Becoming', 'Michelle Obama', '9781524763138', 'Biography', FALSE),
('Sapiens', 'Yuval Noah Harari', '9780062316097', 'History', FALSE),
('The Silent Patient', 'Alex Michaelides', '9781250301697', 'Thriller', FALSE),
('Clean Code', 'Robert C. Martin', '9780132350884', 'Programming', FALSE),
('Python Crash Course', 'Eric Matthes', '9781593279288', 'Programming', FALSE),
('Deep Work', 'Cal Newport', '9781455586691', 'Self-Help', FALSE),
('Atomic Habits', 'James Clear', '9780735211292', 'Self-Help', FALSE),
('The Art of War', 'Sun Tzu', '9781599869773', 'Strategy', FALSE);