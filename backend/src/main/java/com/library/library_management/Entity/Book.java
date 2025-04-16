package main.java.com.library.library_management.Entity;

import javax.persistence.*;

public class Book {
    @Id
    private String isbn;
    private String title;
    private String genre;
    private int pubYear;
    private boolean availStatus;

    @ManyToOne
    @JoinColumn(name = "author_id")
    private Author author;

    // Getters and Setters
    public String getIsbn() { return isbn; }
    public void setIsbn(String isbn) { this.isbn = isbn; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getGenre() { return genre; }
    public void setGenre(String genre) { this.genre = genre; }
    public int getPubYear() { return pubYear; }
    public void setPubYear(int pubYear) { this.pubYear = pubYear; }
    public boolean isAvailStatus() { return availStatus; }
    public void setAvailStatus(boolean availStatus) { this.availStatus = availStatus; }
    public Author getAuthor() { return author; }
    public void setAuthor(Author author) { this.author = author; }
}

