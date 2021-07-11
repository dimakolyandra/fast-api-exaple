from sql_app.models import SessionLocal


def get_db():
    db = SessionLocal()
    yield db

