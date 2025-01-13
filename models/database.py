from sqlmodel import Field, SQLModel, create_engine
from .model import *

# Definição do banco de dados
sqllite_file_name = "database.db"
sqllite_url = f'sqlite:///{sqllite_file_name}'

# Criação da engine
engine = create_engine(sqllite_url, echo=True)

if __name__ == "__main__":
    # Criação do banco de dados
    SQLModel.metadata.create_all(engine)