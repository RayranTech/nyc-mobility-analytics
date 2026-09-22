
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv(override=False)

arquivo = "data/raw/yellow_tripdata_2024-01.parquet"

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

try:
    tabela_existe = inspect(engine).has_table(
        "yellow_trips",
        schema="raw",
    )

    if tabela_existe:
        with engine.connect() as conn:
            total = conn.execute(
                text("SELECT COUNT(*) FROM raw.yellow_trips")
            ).scalar()

        if total > 0:
            print(f"Tabela já carregada: {total:,} registros.")
            print("Carga ignorada para evitar duplicação.")
        else:
            df = pd.read_parquet(arquivo)
            print(f"Carregando {len(df):,} registros...")

            df.to_sql(
                name="yellow_trips",
                con=engine,
                schema="raw",
                if_exists="append",
                index=False,
                chunksize=10_000,
            )

            print("Carga concluída!")
    else:
        df = pd.read_parquet(arquivo)
        print(f"Carregando {len(df):,} registros...")

        df.to_sql(
            name="yellow_trips",
            con=engine,
            schema="raw",
            if_exists="append",
            index=False,
            chunksize=10_000,
        )

        print("Carga concluída!")

finally:
    engine.dispose()
