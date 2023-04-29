from sqlalchemy import create_engine


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)  # БД в оперативке
#engine = create_engine("sqlite+pysqlite:///sqlite3.db", echo=False, max_overflow=100)  # БД в локальная sqlite
# engine = create_engine(CONNECTION_STRING, echo=False, max_overflow=100)
