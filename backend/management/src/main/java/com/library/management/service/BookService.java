package com.library.management.service;

import com.library.management.entity.Book;
import com.library.management.repository.BookRepository;

public class BookService {
    @Autowired
    private BookRepository bookRepository;

    public Book addBook(Book book) {
        return bookRepository.save(book);
    }

    public Book getBook(String ISBN) {
        return bookRepository.findById(ISBN).orElse(null);
    }

    public List<Book> getAllBooks() {
        return bookRepository.findAll();
    }

    // Get Book by ISBN
    public Book getBookByIsbn(String isbn) {
        return bookRepository.findByIsbn(isbn);
    }

    // Get Book by ID
    public Optional<Book> getBookById(Long id) {
        return bookRepository.findById(id);
    }

    // Delete Book by ID
    public void deleteBook(Long id) {
        bookRepository.deleteById(id);
    }
}