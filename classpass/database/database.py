from sys import argv, exit
import sys
import os

# Include the project directory in the Python path (problems with database dir)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models0 import Base
from populate import main as populate_main

DATABASE = rf"sqlite:///classpass/database/classpass.db"

engine = create_engine(DATABASE)
Session = sessionmaker(bind=engine)
session = Session()

def main():  
    if len(argv) == 3 and argv[1] == "-c":
        if argv[2] == "-models":
            Base.metadata.create_all(bind=engine)
            print("Models created.")
            exit(0)
        elif argv[2] == "-populate":
            populate_main(session)
            print("Models populated.")
            exit(0)
        else:
            print("Invalid Argument.")
            exit(1)

if __name__ == "__main__":
    main()
