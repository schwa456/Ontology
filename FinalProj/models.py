from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = 'mysql+pymysql://root:94959495p!!@localhost/db_name'

engine = create_engine(DB_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define Heritage Table
class Heritage(Base):
    __tablename__ = 'heritage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text)
    designated_date = Column(Date)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()