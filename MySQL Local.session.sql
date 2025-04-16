CREATE DATABASE IF NOT EXISTS library_system;
USE library_system;

CREATE TABLE Author (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Book (
    ISBN VARCHAR(13) PRIMARY KEY,
    author INT,
    genre VARCHAR(255),
    title VARCHAR(255),
    pub_year INT,
    avail_status BOOLEAN,
    FOREIGN KEY (author) REFERENCES Author(ID)
);

CREATE TABLE Librarian (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Librarian_phone (
    ID INT,
    phone VARCHAR(15),
    FOREIGN KEY (ID) REFERENCES Librarian(ID)
);

CREATE TABLE Member (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    borrow_hist TEXT
);

CREATE TABLE Member_phone (
    ID INT,
    phone VARCHAR(15),
    FOREIGN KEY (ID) REFERENCES Member(ID)
);

CREATE TABLE Write (
    Author_ID INT,
    ISBN VARCHAR(13),
    FOREIGN KEY (Author_ID) REFERENCES Author(ID),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    PRIMARY KEY (Author_ID, ISBN)
);

CREATE TABLE Catalog (
    ISBN VARCHAR(13),
    Librarian_ID INT,
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    FOREIGN KEY (Librarian_ID) REFERENCES Librarian(ID),
    PRIMARY KEY (ISBN, Librarian_ID)
);

CREATE TABLE Borrow (
    Member_ID INT,
    ISBN VARCHAR(13),
    FOREIGN KEY (Member_ID) REFERENCES Member(ID),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    PRIMARY KEY (Member_ID, ISBN)
);

CREATE TABLE Issue_receive (
    Member_ID INT,
    Librarian_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES Member(ID),
    FOREIGN KEY (Librarian_ID) REFERENCES Librarian(ID),
    PRIMARY KEY (Member_ID, Librarian_ID)
);

