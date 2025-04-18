package com.library.management.entity;

import jakarta.persistence.*;

@Entity
public class Author {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)

        private Long id;   
        private String name;
     
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Author{" +
                "authorid=" + authorid +
                ", name='" + name + '\'' +
                '}';
    }
}

