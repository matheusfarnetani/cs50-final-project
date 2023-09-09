from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, Cards, Visitants

# TODO - Create main function with kwargs to run normally without creating but when execute with -create it creates tables

# Create Engine
engine = create_engine(rf"sqlite:///my_database.db")

# Create tables
Base.metadata.create_all(bind=engine)

# Attach sessionmaker into Session
Session = sessionmaker(bind=engine)

# Create Session object
session = Session()

# pedro_card = Cards(uid="AA AA AA AA", type="visitant")
# pedro = Visitants(name="pedro", birthday=date(2000, 3, 4), document="1234567890", card_id=1)
# session.add(pedro_card)
# session.add(pedro)
# session.commit()