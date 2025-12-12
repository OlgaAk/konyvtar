from flask import Flask
from models.Book import Book
from db import db
from routes.main import main_bp
    
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "supersecret"
    db.init_app(app)

    with app.app_context():
        print(db.inspect(db.engine).get_table_names())
        db.create_all()
        
    app.register_blueprint(main_bp)

    return app