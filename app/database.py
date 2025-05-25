from databases import Database
import sqlalchemy

DATABASE_URL = "sqlite:///./todo.db"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
