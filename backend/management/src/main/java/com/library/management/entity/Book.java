package com.library.management.entity;

import jakarta.persistence.*;

@Entity
public class Book {
      @Id
    private String isbn;
    private String title;
    private String genre;
    private int pubYear;
    private boolean availStatus;

    @ManyToOne
    private Author author;
    
    // Getters and Setters
}


