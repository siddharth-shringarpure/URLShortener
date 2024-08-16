from flask import Flask
from .db import db
from .urlshort import bp
import os, stat
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    my_app = Flask(__name__)
    my_app.secret_key = os.getenv("SECRET_KEY")

    # Ensure the directory exists
    db_dir = os.path.join(os.getcwd(), "urlshort")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_path = os.path.join(db_dir, 'db.sqlite3')

    my_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not os.path.exists(db_path):
        open(db_path, 'a').close()  # Create the file if it doesn't exist
    os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)  # Ensure owner has read and write permissions

    db.init_app(my_app)

    my_app.register_blueprint(bp)

    with my_app.app_context():  # Needed to create the tables
        try:
            db.create_all()
            print("Tables created")
        except Exception as e:
            print(f"Error creating tables: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Database file path: {os.path.join(os.getcwd(), 'urlshort/db.sqlite3')}")

    return my_app


app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run()
