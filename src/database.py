from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy
from datatypes import Movie, Character, Conversation, Line

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = create_engine(database_connection_url())

# Create a single connection to the database
conn = engine.connect()

result = conn.execute(sqlalchemy.text("SELECT * FROM movies"))
movies = {
    row["movie_id"]: Movie(row["movie_id"],
                    row["title"], 
                    row["year"], 
                    row["imdb_rating"], 
                    row["imdb_votes"], 
                    row["raw_script_url"])
    for row in result
}