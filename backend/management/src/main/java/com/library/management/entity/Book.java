package com.library.management.entity;

import jakarta.persistence.*;

@Entity
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer book_id;
    private String title;
    private String genre;
    private Integer publication_year;
    private String isbn;

    @ManyToOne
    @JoinColumn(name = "author_id")
    private Author author;
}