from sys import argv, exit
import sys
import os

# Include the project directory in the Python path (problems with database dir)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

import models
from populate import main as populate_main
from app import create_app, db

DB_NAME = "classpass"
DATABASE = rf"sqlite:///{DB_NAME}.db"

def main():
    app = create_app()
    with app.app_context():    
        if len(argv) == 3 and argv[1] == "-c":
            if argv[2] == "-models":
                models.db.create_all()
                print("Models created.")
                exit(0)
            elif argv[2] == "-populate":
                populate_main(db=db)
                print("Models populated.")
                exit(0)
            else:
                print("Invalid Argument.")
                exit(1)

if __name__ == "__main__":
    main()
