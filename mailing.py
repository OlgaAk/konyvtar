import os
import requests

from models.Book import Book

MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')  
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')  

def notify_book_status_change(books: list[Book], to_email: str):
    status = ""
    for book in books:
        for printed_book in book.printed_books:
            if printed_book.changed:
                status += f'Book: {book.name}, Address: {printed_book.address}, New Status: {printed_book.status}\n'
    if status != "":
        send_mail(status, to_email)
        

def send_mail(status: str, to_email: str):
    if not to_email:
        return
    else:
        return requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", os.getenv('API_KEY', MAILGUN_API_KEY)),
            data={"from": f"{SENDER_EMAIL}",
                "to": to_email,
                "subject": "Loaned book status changed",
                "text": f"New status: {status}"})     
