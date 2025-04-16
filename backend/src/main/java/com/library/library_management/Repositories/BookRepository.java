package main.java.com.library.library_management.Repositories;

import com.library.management.model.Book;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BookRepository extends JpaRepository<Book, String> {
}

