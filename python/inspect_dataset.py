import pyarrow.parquet as pq

arquivo = "data/raw/yellow_tripdata_2024-01.parquet"

parquet = pq.ParquetFile(arquivo)

print("=" * 50)
print("INFORMAÇÕES DO DATASET")
print("=" * 50)

print(f"Linhas: {parquet.metadata.num_rows}")
print(f"Colunas: {parquet.metadata.num_columns}")

print("\nCOLUNAS E TIPOS:")
print(parquet.schema_arrow)