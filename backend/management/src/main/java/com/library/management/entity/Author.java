package com.library.management.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "authors")
public class Author {
    
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
    
        private String name;
    
        @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
        private List<Book> books;
}
