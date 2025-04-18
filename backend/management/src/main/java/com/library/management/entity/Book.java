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

    public Long getId() {
    return id;
}

    public void setId(Long id) {
    this.id = id;
}

    public String getIsbn() {
    return isbn;
}

    public void setIsbn(String isbn) {
    this.isbn = isbn;
}

    public String getTitle() {
    return title;
}

    public void setTitle(String title) {
    this.title = title;
}

    public String getAuthor() {
    return author;
}

    public void setAuthor(String author) {
    this.author = author;
}

    public String getGenre() {
    return genre;
}

    public void setGenre(String genre) {
    this.genre = genre;
}

    public int getPublicationYear() {
    return pubYear;
}

    public void setPublicationYear(int publicationYear) {
    this.pubYear = publicationYear;
}

    public boolean isAvailStatus() {
    return availStatus;
}

    public void setAvailStatus(boolean availStatus) {
    this.availStatus = availStatus;
  }
}
    
