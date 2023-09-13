from sys import argv, exit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import database.models as models
from database.populate import main as populate_main


DB_NAME = "classpass"
DATABASE = rf"sqlite:///database/{DB_NAME}.db"

# https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
engine = create_engine(DATABASE, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


if __name__ == "__main__":
    # Arguments
    if len(argv) == 3 and argv[1] == "-c":
        engine = create_engine(DATABASE)
        # Create Engine
        if argv[2] == "-models":
            # Create tables
            models.Base.metadata.create_all(bind=engine)
            print("Models created.")
            exit(0)
        elif argv[2] == "-populate":
            # Execute populate
            populate_main(sessionLocal=sessionLocal)
            print("Models populated.")
            exit(0)
        else:
            # Wrong argument :/
            print("Invalid Argument.")
            exit(1)
