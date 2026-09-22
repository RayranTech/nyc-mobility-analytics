
from pathlib import Path
from urllib.request import urlretrieve

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"

DESTINO = Path("data/raw/yellow_tripdata_2024-01.parquet")


def main():
    DESTINO.parent.mkdir(parents=True, exist_ok=True)

    if DESTINO.exists() and DESTINO.stat().st_size > 0:
        print(f"Arquivo já existe: {DESTINO}")
        print("Download ignorado.")
        return

    print("Baixando dados do NYC Taxi...")

    try:
        urlretrieve(URL, DESTINO)
    except Exception:
        DESTINO.unlink(missing_ok=True)
        raise

    print(f"Download concluído: {DESTINO}")


if __name__ == "__main__":
    main()
