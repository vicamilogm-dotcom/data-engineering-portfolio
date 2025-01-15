from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import pgvector.sqlalchemy

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    release_year = Column(Integer)
    title = Column(String)
    origin_ethnicity = Column(String)
    director = Column(String)
    cast = Column(Text)
    genre = Column(String)
    wiki_page = Column(String)
    plot = Column(Text)
    plot_vector = Column(pgvector.sqlalchemy.Vector(dim=128))


if __name__ == "__main__":
    pass  # YOUR CODE HERE
