"""
Task 3: Library Checkout System

Write a Python module for a small library that tracks books, members, and loans.

Classes
- Book(book_id, title) stores a book's ID and title.
- Member(member_id, name) stores a member's ID and name.
- Library() manages books, members, and loans.

Library methods
- add_book(book): add a Book. If a book with the same book_id already exists, raise ValueError.
- add_member(member): add a Member. If a member with the same member_id already exists, raise ValueError.
- checkout(member_id, book_id, checkout_date): lend the book to the member and return the due date.
- return_book(book_id, return_date): end the loan and return the late fee as a float.
- is_available(book_id): return True if the book is not on loan, otherwise False.
- books_on_loan(member_id): return a list of the book_ids the member currently has, in the order they were checked out.

Rules
- The loan period is 14 days. The due date is checkout_date plus 14 days.
- The late fee is 0.25 for each day the book is returned after the due date. Returning on or before the due date costs 0.0.
- The late fee is never more than 10.0.
- A member can have at most 3 books on loan at the same time.
- Dates are datetime.date objects passed in as arguments. Do not use today's date.

Inputs
- book_id, title, member_id, and name must be strings. If not, raise TypeError. If a string is empty, raise ValueError.
- checkout_date and return_date must be datetime.date objects. If not, raise TypeError.

Errors
- Unknown member_id or book_id: raise KeyError.
- Checking out a book that is already on loan: raise ValueError.
- Checking out a 4th book while a member has 3: raise ValueError.
- Returning a book that is not on loan: raise ValueError.
- A return_date before the checkout_date: raise ValueError.

Other
- Do not print anything. Only return values or raise errors.
- Use only the Python standard library. Do not use eval or exec.

"""
from datetime import date, datetime, timedelta

LOAN_PERIOD_DAYS = 14
LATE_FEE_PER_DAY = 0.25
MAX_LATE_FEE = 10.0
MAX_BOOKS_PER_MEMBER = 3


def _check_string(value, field_name):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if value == "":
        raise ValueError(f"{field_name} must not be empty")


def _check_date(value, field_name):
    if not isinstance(value, date) or isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime.date")


class Book:
    def __init__(self, book_id, title):
        _check_string(book_id, "book_id")
        _check_string(title, "title")
        self.book_id = book_id
        self.title = title


class Member:
    def __init__(self, member_id, name):
        _check_string(member_id, "member_id")
        _check_string(name, "name")
        self.member_id = member_id
        self.name = name


class Library:
    def __init__(self):
        self._books = {}
        self._members = {}
        self.loans = {}

    def add_book(self, book):
        if not isinstance(book, Book):
            raise TypeError("book must be a Book")
        if book.book_id in self._books:
            raise ValueError(f"book {book.book_id!r} already exists")
        self._books[book.book_id] = book

    def add_member(self, member):
        if not isinstance(member, Member):
            raise TypeError("member must be a Member")
        if member.member_id in self._members:
            raise ValueError(f"member {member.member_id!r} already exists")
        self._members[member.member_id] = member

    def checkout(self, member_id, book_id, checkout_date):
        _check_string(member_id, "member_id")
        _check_string(book_id, "book_id")
        _check_date(checkout_date, "checkout_date")

        if member_id not in self._members:
            raise KeyError(member_id)
        if book_id not in self._books:
            raise KeyError(book_id)
        if book_id in self.loans:
            raise ValueError(f"book {book_id!r} is already on loan")
        if len(self.books_on_loan(member_id)) >= MAX_BOOKS_PER_MEMBER:
            raise ValueError(f"member {member_id!r} already has "
                             f"{MAX_BOOKS_PER_MEMBER} books on loan")

        due_date = checkout_date + timedelta(days=LOAN_PERIOD_DAYS)
        self.loans[book_id] = {
            "member_id": member_id,
            "checkout_date": checkout_date,
            "due_date": due_date,
        }
        return due_date

    def return_book(self, book_id, return_date):
        _check_string(book_id, "book_id")
        _check_date(return_date, "return_date")

        if book_id not in self._books:
            raise KeyError(book_id)
        if book_id not in self.loans:
            raise ValueError(f"book {book_id!r} is not on loan")

        loan = self.loans[book_id]
        if return_date < loan["checkout_date"]:
            raise ValueError("return_date is before checkout_date")

        del self.loans[book_id]
        days_late = max(0, (return_date - loan["due_date"]).days)
        return float(min(days_late * LATE_FEE_PER_DAY, MAX_LATE_FEE))

    def is_available(self, book_id):
        _check_string(book_id, "book_id")
        if book_id not in self._books:
            raise KeyError(book_id)
        return book_id not in self.loans

    def books_on_loan(self, member_id):
        _check_string(member_id, "member_id")
        if member_id not in self._members:
            raise KeyError(member_id)
        return [book_id for book_id, loan in self.loans.items()
                if loan["member_id"] == member_id]
