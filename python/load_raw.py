import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

arquivo = "data/raw/yellow_tripdata_2024-01.parquet"

df = pd.read_parquet(arquivo)

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

print(f"Dataset carregado: {len(df):,} linhas")
print("Iniciando carga no PostgreSQL...")

df.to_sql(
    name="yellow_trips",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False,
    chunksize=10_000
)

print("Carga concluída!")

engine.dispose()