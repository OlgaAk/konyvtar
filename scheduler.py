from apscheduler.schedulers.blocking import BlockingScheduler
import os
from compare import compare_books
from file_helper import load_from_file, save_to_file
from models.Book import Book
import scrape
from mailing import notify_book_status_change


def scheduled_job():
    print("Loading saved books")
    chached_books_dict: list[Book] = load_from_file()
    
    print("Converting to Book objects")
    chached_books = [Book.from_dict(b) for b in chached_books_dict] 
    
    print("Fetching current books")
    books: list[Book] = scrape.scrape()
    
    print("Saving current books")
    save_to_file([b.to_dict() for b in books])
    
    print("Comparing books")
    compare_books(books, chached_books)
    
    print("Notifying about book status changes")
    notify_book_status_change(books, os.environ.get('NOTIFY_EMAIL', ''))



if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Run every 2 hours
    scheduler.add_job(scheduled_job, 'cron', hour='8-23/2')
    print("Scheduler started...")
    scheduler.start()