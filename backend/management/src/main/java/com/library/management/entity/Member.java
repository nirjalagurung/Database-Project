package com.library.management.entity;

import jakarta.persistence.*;

public class Member {
     @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String borrowHist;
}
