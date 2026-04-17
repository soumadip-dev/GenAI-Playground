from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

# Initialize FastAPI application
app = FastAPI(title="Todo API", version="1.0.0")

# SQLite database URL
DATABASE_URL = "sqlite:///./test.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
)


# Create a configured "SessionLocal" class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# Database model for Todo items
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(String, default="false")


# Create all tables in the database
Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency that provides a database session.
    Ensures the session is closed after request completion.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root(db: Session = Depends(get_db)):
    return {
        "status": "success",
        "message": "FastAPI application is running and SQLite database is connected successfully.",
    }
