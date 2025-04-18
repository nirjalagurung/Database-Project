package com.library.management.entity;

import jakarta.persistence.*;

@Entity
public class Librarian {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;
    
        private String name;
    }


