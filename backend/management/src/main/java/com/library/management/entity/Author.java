package com.library.management.entity;

import jakarta.persistence.*;

@Entity
public class Author {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)

        private Long id;   
        private String name;
        
        @OneToMany(mappedBy = "author")
        private Set<Book> books;
        public Author(int authorid, String name) {
            this.authorid = authorid;
            this.name = name;
        }
        public Author(String name) {
            this.name = name;
        }
        public Author() {
        }
        public int getAuthorid() {
            return authorid;
        }
        public void setAuthorid(int authorid) {
            this.authorid = authorid;
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