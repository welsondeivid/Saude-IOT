from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Nome do arquivo SQLite que será criado na raiz
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# engine: Objeto de conexão com o banco de dados. 
# "check_same_thread": False é necessário apenas para SQLite no FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: Classe de sessão para interagir com o banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Classe base que os modelos (tabelas) do SQLAlchemy irão herdar.
Base = declarative_base()

# Dependência para Injeção de Sessão (Deixa o FastAPI abrir e fechar a conexão)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()