CREATE DATABASE LibraryManagement;
USE LibraryManagement;

CREATE TABLE Author (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
);

CREATE TABLE Book (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    genre VARCHAR(50),
    publication_year INT,
    isbn VARCHAR(20) UNIQUE,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

INSERT INTO Book (title, genre, publication_year, isbn, author_id) VALUES 
('Harry Potter and the Sorcerer''s Stone', 'Fantasy', 1997, '978-0439708180', 1),
('1984', 'Dystopian', 1949, '978-0451524935', 2),
('To Kill a Mockingbird', 'Classic', 1960, '978-0061120084', 3),
('The Great Gatsby', 'Classic', 1925, '978-0743273565', 4),
('Pride and Prejudice', 'Romance', 1813, '978-1503290563', 5),
('Harry Potter and the Chamber of Secrets', 'Fantasy', 1998, '978-0439064873', 1);


CREATE TABLE Member (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
);

INSERT INTO Member (name, email) VALUES 
('Alice Johnson', 'alice.j@example.com'),
('Bob Smith', 'bob.s@example.com'),
('Charlie Brown', 'charlie.b@example.com'),
('Diana Prince', 'diana.p@example.com'),
('Ethan Hunt', 'ethan.h@example.com');


CREATE TABLE Borrow (
    borrow_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    member_id INT,
    borrow_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES Book(book_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

INSERT INTO Borrow (book_id, member_id, borrow_date, return_date) VALUES 
(1, 1, '2023-03-01', '2023-03-15'),
(2, 1, '2023-03-16', NULL),
(3, 2, '2023-03-05', '2023-03-25'),
(4, 3, '2023-04-10', NULL),
(5, 4, '2023-04-15', NULL),
(6, 5, '2023-05-01', NULL),
(2, 3, '2023-05-03', NULL);

