import pandas as pd
import streamlit as st
import pymysql

#DATABASE CONNECTION
def create_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='koromjaner',
        database='libraryDB'
    )
#AUTHENTICATION
def login_user(username, password, is_admin=False):
    conn = create_connection()
    cursor = conn.cursor()
    table = "admin" if is_admin else "users"
    cursor.execute(f"SELECT * FROM {table} WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def signup_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()

#BOOK RECOMMENDATION FUNCTION
def recommend_books(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT b.category
            FROM books b
            JOIN borrow br ON b.book_id = br.book_id
            WHERE br.user_id = %s AND br.returned = 1
        """, (user_id,))
        borrowed_categories = cursor.fetchall()
        
        if not borrowed_categories:
            return []
        
        categories = [cat[0] for cat in borrowed_categories]

        placeholders = ', '.join(['%s'] * len(categories))
        query = f"""
            SELECT book_id, title, author, isbn, category
            FROM books
            WHERE category IN ({placeholders}) AND is_borrowed = 0
        """
        cursor.execute(query, tuple(categories))
        recommended_books = cursor.fetchall()

    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
        recommended_books = []

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return recommended_books

#USER DASHBOARD 
def user_dashboard():
    st.header("User Dashboard")

    if st.button("Logout"):
        st.session_state["user_id"] = None
        st.session_state["is_admin"] = False
        st.rerun()

    option = st.selectbox(
        "Choose an action", 
        ["Browse Books", "Search Books", "Borrow Book", "Return Book", "My Borrowed Books", "Book Recommendations"]
    )
    if option == "Book Recommendations":
        st.subheader("Book Recommendations Based on Your Borrowing History")
        recommended_books = recommend_books(st.session_state["user_id"])

        if recommended_books:
            books_df = pd.DataFrame(recommended_books, columns=["Book ID", "Title", "Author", "ISBN", "Category"])
            st.table(books_df)
        else:
            st.info("No recommendations available based on your borrowing history.")

    if option == "Browse Books":
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author, isbn, category FROM books WHERE is_borrowed = 0")
            books = cursor.fetchall()
        except Exception as e:
            st.error(f"Error fetching books: {e}")
            books = []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        if books:
            books_df = pd.DataFrame(books, columns=["Book ID", "Title", "Author", "ISBN", "Category"])
            st.table(books_df)
        else:
            st.info("No books available.")

    elif option == "Search Books":
        search_by = st.selectbox("Search by", ["Book ID", "Title", "Author", "ISBN", "Category"])
        query = st.text_input("Enter your search term")

        if st.button("Search"):
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute(f"""
                    SELECT book_id, title, author, isbn, category 
                    FROM books 
                    WHERE {search_by.lower().replace(' ', '_')} LIKE %s
                """, (f"%{query}%",))
                result = cursor.fetchall()
            except Exception as e:
                st.error(f"Error searching books: {e}")
                result = []
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()

            if result:
                result_df = pd.DataFrame(result, columns=["Book ID", "Title", "Author", "ISBN", "Category"])
                st.table(result_df)
            else:
                st.info("No matching books found.")

    elif option == "Borrow Book":
        book_id = st.text_input("Enter Book ID to borrow")

        if st.button("Borrow"):
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT is_borrowed FROM books WHERE book_id = %s", (book_id,))
                book = cursor.fetchone()
                
                if not book:
                    st.error("Book ID not found.")
                elif book[0] == 1:
                    st.warning("This book is already borrowed.")
                else:
                    cursor.execute("""
                        INSERT INTO borrow (user_id, book_id, returned) 
                        VALUES (%s, %s, %s)
                    """, (st.session_state["user_id"], book_id, False))
                    cursor.execute("UPDATE books SET is_borrowed = 1 WHERE book_id = %s", (book_id,))
                    conn.commit()
                    st.success("Book borrowed successfully!")
            except Exception as e:
                st.error(f"Error borrowing book: {e}")
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()

    elif option == "Return Book":
        book_id = st.text_input("Enter Book ID to return")

        if st.button("Return"):
            try:
                conn = create_connection()
                cursor = conn.cursor()
                # Mark the book as returned
                cursor.execute("UPDATE books SET is_borrowed = 0 WHERE book_id = %s", (book_id,))
                cursor.execute("UPDATE borrow SET returned = 1 WHERE book_id = %s AND user_id = %s", (book_id, st.session_state["user_id"]))
                conn.commit()
                st.success("Book returned successfully!")
            except Exception as e:
                st.error(f"Error returning book: {e}")
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()

    elif option == "My Borrowed Books":
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    b.book_id AS "Book ID", 
                    b.title AS "Title", 
                    b.author AS "Author", 
                    b.category AS "Category", 
                    CASE 
                        WHEN br.returned = 0 THEN 'Borrowed'
                        WHEN br.returned = 1 THEN 'Returned'
                        ELSE 'Unknown'
                    END AS "Borrow Status",
                    CASE 
                        WHEN br.returned = 0 THEN 'Not Returned'
                        WHEN br.returned = 1 THEN 'Returned'
                        ELSE 'Unknown'
                    END AS "Return Status"
                FROM books b
                JOIN borrow br ON b.book_id = br.book_id
                WHERE br.user_id = %s
            """, (st.session_state["user_id"],))
            borrowed_books = cursor.fetchall()
        except Exception as e:
            st.error(f"Error fetching borrowed books: {e}")
            borrowed_books = []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        if borrowed_books:
            borrowed_books_df = pd.DataFrame(
                borrowed_books,
                columns=["Book ID", "Title", "Author", "Category", "Borrow Status", "Return Status"]
            )
            st.subheader("Books You Borrowed")
            st.table(borrowed_books_df)
        else:
            st.info("You have not borrowed any books.")

#ADMIN DASHBOARD
def admin_dashboard():
    st.header("Admin Dashboard")

    if st.button("Logout"):
        st.session_state["user_id"] = None
        st.session_state["is_admin"] = False
        st.rerun()

    option = st.selectbox("Choose an action", ["Available Books", "Add New Book", "Edit or Delete a Book", "User Management"])

    if option == "Available Books":
        st.subheader("Available Books")

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id, title, author, isbn, category, is_borrowed FROM books")
        all_books = cursor.fetchall()
        conn.close()

        books_dict = [{"book_id": book[0], "title": book[1], "author": book[2], "isbn": book[3], "category": book[4], "is_borrowed": book[5]} for book in all_books]
        books_df = pd.DataFrame(books_dict)

        st.dataframe(books_df)

    elif option == "Add New Book":
        st.subheader("Add New Book")

        book_id = st.text_input("New Book ID")
        title = st.text_input("New Book Title")
        author = st.text_input("New Book Author")
        isbn = st.text_input("New Book ISBN")
        category = st.text_input("New Book Category")

        if st.button("Add Book"):
            if book_id and title and author and isbn and category:
                try:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO books (book_id, title, author, isbn, category, is_borrowed) 
                        VALUES (%s, %s, %s, %s, %s, 0)
                    """, (book_id, title, author, isbn, category))
                    conn.commit()
                    conn.close()
                    st.success("New book added successfully!")
                    st.experimental_rerun()
                except pymysql.MySQLError as err:
                    st.error(f"Error: {err}")
            else:
                st.warning("Please fill out all fields before adding a new book.")

    elif option == "Edit or Delete a Book":
        st.subheader("Edit or Delete a Book")

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id, title, author, isbn, category, is_borrowed FROM books")
        all_books = cursor.fetchall()
        conn.close()

        book_options = {f"{book[1]} (ID: {book[0]})": book[0] for book in all_books}

        if book_options:
            selected_book_label = st.selectbox("Select a Book to Edit/Delete", list(book_options.keys()))
            selected_book_id = book_options[selected_book_label]

            new_title = st.text_input("New Title (leave blank to keep same)")
            new_author = st.text_input("New Author (leave blank to keep same)")
            new_isbn = st.text_input("New ISBN (leave blank to keep same)")
            new_category = st.text_input("New Category (leave blank to keep same)")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Edit Book"):
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT title, author, isbn, category FROM books WHERE book_id=%s", (selected_book_id,))
                    existing = cursor.fetchone()

                    if existing:
                        title = new_title if new_title else existing[0]
                        author = new_author if new_author else existing[1]
                        isbn = new_isbn if new_isbn else existing[2]
                        category = new_category if new_category else existing[3]

                        cursor.execute("""
                            UPDATE books 
                            SET title=%s, author=%s, isbn=%s, category=%s 
                            WHERE book_id=%s
                        """, (title, author, isbn, category, selected_book_id))
                        conn.commit()
                        conn.close()
                        st.success("Book updated successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Book not found!")

            with col2:
                if st.button("Delete Book"):
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM books WHERE book_id=%s", (selected_book_id,))
                    conn.commit()
                    conn.close()
                    st.success("Book deleted successfully!")
                    st.experimental_rerun()
        else:
            st.warning("No books available to edit or delete.")

    elif option == "User Management":
        st.subheader("User Borrow/Return Summary")

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.username,
                   COUNT(br.borrow_id) AS total_borrowed,
                   SUM(CASE WHEN br.returned IS NOT NULL THEN 1 ELSE 0 END) AS total_returned,
                   SUM(CASE WHEN br.returned IS NULL THEN 1 ELSE 0 END) AS total_not_returned
            FROM users u
            LEFT JOIN borrow br ON u.user_id = br.user_id
            GROUP BY u.username
        """)
        user_borrow_info = cursor.fetchall()
        conn.close()

        if user_borrow_info:
            user_borrow_df = pd.DataFrame(user_borrow_info, columns=["Username", "Total Borrowed", "Total Returned", "Currently Borrowed"])
            st.dataframe(user_borrow_df)

            selected_user = st.selectbox("Select User to View Borrowed Books", [user[0] for user in user_borrow_info])
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.title AS "Book Title", b.author AS "Author", 
                   CASE 
                        WHEN br.returned IS NULL OR br.returned = 0 THEN 'Not Returned' 
                        WHEN br.returned IS NOT NULL AND br.returned != 0 THEN 'Returned'
                        ELSE 'Unknown Status' 
                        END AS "Return Status"
            FROM borrow br
            JOIN books b ON br.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            WHERE u.username = %s
        """, (selected_user,))
        borrowed_books = cursor.fetchall()
        conn.close()

        if borrowed_books:
            borrowed_books_df = pd.DataFrame(borrowed_books, columns=["Book Title", "Author", "Return Status"])
            st.subheader(f"Books Borrowed by {selected_user}")
            st.dataframe(borrowed_books_df)                   
        else:
            st.warning(f"{selected_user} has not borrowed any books.")
    else:
        st.info("No users or borrow records found.")

#MAIN APP
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

st.title("Library Management System")

if st.session_state["user_id"]:
    if st.session_state["is_admin"]:
        admin_dashboard()
    else:
        user_dashboard()

else:
    menu = st.sidebar.selectbox("Menu", ["User Login", "Admin Login", "Sign Up"])

    if menu == "User Login":
        st.subheader("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("User Login"):
            user = login_user(username, password)
            if user:
                st.session_state["user_id"] = user[0]
                st.session_state["is_admin"] = False
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    elif menu == "Admin Login":
        st.subheader("Admin Login")
        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")
        if st.button("Login as Admin"):
            admin = login_user(username, password, is_admin=True)
            if admin:
                st.session_state["user_id"] = admin[0]
                st.session_state["is_admin"] = True
                st.rerun()()
            else:
                st.error("Invalid admin credentials")

    elif menu == "Sign Up":
        st.subheader("Create an Account")
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Sign Up"):
            signup_user(username, password)
            st.success("Account created successfully! Please login.")
