class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {'Available' if self.available else 'Not Available'}"


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book)
            return f"{self.name} borrowed {book.title}."
        return f"{book.title} is not available."

    def return_book(self, book):
        if book in self.borrowed_books:
            book.available = True
            self.borrowed_books.remove(book)
            return f"{self.name} returned {book.title}."
        return f"{self.name} did not borrow {book.title}."

    def list_borrowed_books(self):
        if not self.borrowed_books:
            return f"{self.name} has not borrowed any books."
        return f"{self.name} has borrowed: " + ", ".join(book.title for book in self.borrowed_books)


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


# Example usage
if __name__ == "__main__":
    library = Library()
    book1 = Book("1984", "George Orwell", "123456789")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "987654321")
    library.add_book(book1)
    library.add_book(book2)

    member1 = Member("Alice", "001")
    library.register_member(member1)

    print(library.loan_book(member1, book1))
    print(library.list_available_books())
    print(member1.list_borrowed_books())
    print(library.return_book(member1, book1))
    print(library.list_available_books())
    print(library.search_book(title="1984"))
    print(library.list_all_members())