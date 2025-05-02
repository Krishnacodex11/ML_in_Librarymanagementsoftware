from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.due_date = None
        self.reserved_by = []

    def __str__(self):
        status = "Available" if self.available else f"Not Available (Due: {self.due_date.strftime('%Y-%m-%d')})"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status}"

class Member:
    MAX_BORROW_LIMIT = 3

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.history = []

    def borrow_book(self, book):
        if len(self.borrowed_books) >= Member.MAX_BORROW_LIMIT:
            return f"{self.name} has reached the borrow limit ({Member.MAX_BORROW_LIMIT})."

        if book.available:
            book.available = False
            book.due_date = datetime.now() + timedelta(days=14)
            self.borrowed_books.append(book)
            self.history.append((book.title, "Borrowed", datetime.now().strftime('%Y-%m-%d')))
            return f"{self.name} borrowed {book.title}. Due date: {book.due_date.strftime('%Y-%m-%d')}"
        else:
            if self not in book.reserved_by:
                book.reserved_by.append(self)
                return f"{book.title} is not available. {self.name} has been added to the reservation list."
            else:
                return f"{self.name} has already reserved {book.title}."

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.available = True
            fine = 0
            if datetime.now() > book.due_date:
                days_late = (datetime.now() - book.due_date).days
                fine = days_late * 2  # ₹2 per day late
            self.history.append((book.title, "Returned", datetime.now().strftime('%Y-%m-%d')))
            book.due_date = None

            # Handle reservation queue
            if book.reserved_by:
                next_member = book.reserved_by.pop(0)
                next_member.borrow_book(book)

            return f"{self.name} returned {book.title}. Fine: ₹{fine}" if fine > 0 else f"{self.name} returned {book.title}."
        return f"{self.name} did not borrow {book.title}."

    def list_borrowed_books(self):
        if not self.borrowed_books:
            return f"{self.name} has not borrowed any books."
        return f"{self.name} has borrowed:\n" + "\n".join(f"{book.title} (Due: {book.due_date.strftime('%Y-%m-%d')})" for book in self.borrowed_books)

    def view_borrowing_history(self):
        if not self.history:
            return f"No borrowing history for {self.name}."
        return f"History for {self.name}:\n" + "\n".join(f"{entry[0]} - {entry[1]} on {entry[2]}" for entry in self.history)


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def register_member(self, member):
        self.members.append(member)

    def loan_book(self, member, book):
        if book in self.books and member in self.members:
            return member.borrow_book(book)
        return "Book or member not found."

    def return_book(self, member, book):
        if book in self.books and member in self.members:
            return member.return_book(book)
        return "Book or member not found."

    def list_available_books(self):
        available_books = [str(book) for book in self.books if book.available]
        return "Available books:\n" + "\n".join(available_books) if available_books else "No available books."

    def search_book(self, title=None, author=None, isbn=None):
        results = []
        for book in self.books:
            if (title and title.lower() in book.title.lower()) or \
               (author and author.lower() in book.author.lower()) or \
               (isbn and isbn == book.isbn):
                results.append(str(book))
        return "Search results:\n" + "\n".join(results) if results else "No books found."

    def list_all_members(self):
        return "Registered members:\n" + "\n".join(f"{member.name} (ID: {member.member_id})" for member in self.members) if self.members else "No members registered."

    def list_all_borrowed_books(self):
        borrowed_list = []
        for member in self.members:
            for book in member.borrowed_books:
                borrowed_list.append(f"{book.title} borrowed by {member.name} (Due: {book.due_date.strftime('%Y-%m-%d')})")
        return "Borrowed books:\n" + "\n".join(borrowed_list) if borrowed_list else "No books are currently borrowed."

# Load books from file
try:
    with open("books.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 4:
                isbn,title,author,year = parts
                Library.add_book(Book(isbn.strip(), title.strip(), author.strip(),year.strip()))
except FileNotFoundError:
    print("books.txt not found. Please ensure it exists in the same directory.")

if __name__ == "__main__":
    library = Library()

    # Add initial books
    library.add_book(Book("1984", "George Orwell", "123456789"))
    library.add_book(Book("To Kill a Mockingbird", "Harper Lee", "987654321"))
    library.add_book(Book("Brave New World", "Aldous Huxley", "111222333"))

    # Register initial members
    member1 = Member("Alice", "001")
    member2 = Member("Bob", "002")
    library.register_member(member1)
    library.register_member(member2)

    # Select active member (for simplicity)
    current_member = member1

    while True:
        print("\n===== Library Menu =====")
        print("1. Search Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. View Borrowed Books")
        print("5. View Borrowing History")
        print("6. View Available Books")
        print("7. View All Borrowed Books")
        print("8. Register New Member")
        print("9. Switch Member")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title (or leave blank): ")
            author = input("Enter author name (or leave blank): ")
            isbn = input("Enter ISBN (or leave blank): ")
            print(library.search_book(title if title else None, author if author else None, isbn if isbn else None))

        elif choice == '2':
            title = input("Enter the title of the book to borrow: ")
            book = next((b for b in library.books if b.title.lower() == title.lower()), None)
            if book:
                print(library.loan_book(current_member, book))
            else:
                print("Book not found.")

        elif choice == '3':
            title = input("Enter the title of the book to return: ")
            book = next((b for b in library.books if b.title.lower() == title.lower()), None)
            if book:
                print(library.return_book(current_member, book))
            else:
                print("Book not found.")

        elif choice == '4':
            print(current_member.list_borrowed_books())

        elif choice == '5':
            print(current_member.view_borrowing_history())

        elif choice == '6':
            print(library.list_available_books())

        elif choice == '7':
            print(library.list_all_borrowed_books())

        elif choice == '8':
            name = input("Enter new member's name: ")
            mem_id = input("Enter new member ID: ")
            new_member = Member(name, mem_id)
            library.register_member(new_member)
            print(f"Registered new member: {name} (ID: {mem_id})")

        elif choice == '9':
            print("Registered Members:")
            for m in library.members:
                print(f"{m.name} (ID: {m.member_id})")
            mem_id = input("Enter member ID to switch to: ")
            found = next((m for m in library.members if m.member_id == mem_id), None)
            if found:
                current_member = found
                print(f"Switched to member: {current_member.name}")
            else:
                print("Member ID not found.")

        elif choice == '0':
            print("Exiting Library System. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

    
    
    
    
    
    
    