import pandas as pd

arquivo = "data/raw/yellow_tripdata_2024-01.parquet"

df = pd.read_parquet(arquivo)

print("=" * 60)
print("PERFIL DO DATASET")
print("=" * 60)

print(f"\nLinhas: {len(df)}")
print(f"Colunas: {len(df.columns)}")

print("\nPERÍODO:")
print("Início:", df["tpep_pickup_datetime"].min())
print("Fim:", df["tpep_dropoff_datetime"].max())

print("\nNULOS:")
print(df.isna().sum().sort_values(ascending=False))

print("\nESTATÍSTICAS:")
print(df[[
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
]].describe())

print("\nTIPOS DE PAGAMENTO:")
print(df["payment_type"].value_counts().sort_index())

print("\nVALORES NEGATIVOS:")
print("fare_amount:", (df["fare_amount"] < 0).sum())
print("trip_distance:", (df["trip_distance"] < 0).sum())
print("total_amount:", (df["total_amount"] < 0).sum())

print("\nDURAÇÃO DAS VIAGENS:")

duracao = (
    df["tpep_dropoff_datetime"]
    - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

print(duracao.describe())

print("\n" + "=" * 60)
print("INVESTIGAÇÃO DE QUALIDADE")
print("=" * 60)

# Registros com data de embarque fora de janeiro de 2024
fora_janeiro = (
    (df["tpep_pickup_datetime"] < "2024-01-01") |
    (df["tpep_pickup_datetime"] >= "2024-02-01")
)

print("\nEMBARQUES FORA DE JANEIRO/2024:")
print(fora_janeiro.sum())

# Duração negativa
duracao_negativa = duracao < 0

print("\nDURAÇÃO NEGATIVA:")
print(duracao_negativa.sum())

# Duração superior a 24 horas
duracao_extrema = duracao > 1440

print("\nDURAÇÃO MAIOR QUE 24 HORAS:")
print(duracao_extrema.sum())

# Distâncias muito altas
distancia_100 = df["trip_distance"] > 100
distancia_1000 = df["trip_distance"] > 1000

print("\nDISTÂNCIA MAIOR QUE 100:")
print(distancia_100.sum())

print("\nDISTÂNCIA MAIOR QUE 1000:")
print(distancia_1000.sum())

# Amostra de tarifas negativas
print("\nAMOSTRA DE TARIFAS NEGATIVAS:")
print(
    df.loc[
        df["fare_amount"] < 0,
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type"
        ]
    ].head(10)
)

# Amostra dos registros mais antigos
print("\nREGISTROS MAIS ANTIGOS:")
print(
    df[
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount"
        ]
    ]
    .sort_values("tpep_pickup_datetime")
    .head(10)
)

print("\n" + "=" * 60)
print("REGISTROS FORA DE JANEIRO/2024")
print("=" * 60)

print(
    df.loc[
        fora_janeiro,
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type"
        ]
    ].sort_values("tpep_pickup_datetime")
)

print("\n" + "=" * 60)
print("VIAGENS COM DURAÇÃO NEGATIVA")
print("=" * 60)

print(
    df.loc[
        duracao_negativa,
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type"
        ]
    ].sort_values("tpep_pickup_datetime")
)

print("\n" + "=" * 60)
print("DURAÇÃO NEGATIVA POR TIPO DE PAGAMENTO")
print("=" * 60)

print(
    df.loc[
        duracao_negativa,
        "payment_type"
    ].value_counts().sort_index()
)

print("\n" + "=" * 60)
print("DISTÂNCIAS EXTREMAS")
print("=" * 60)

print(
    df.loc[
        df["trip_distance"] > 100,
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type",
            "PULocationID",
            "DOLocationID"
        ]
    ]
    .sort_values("trip_distance", ascending=False)
)

print("\n" + "=" * 60)
print("10 MAIORES DISTÂNCIAS")
print("=" * 60)

print(
    df[
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type",
            "PULocationID",
            "DOLocationID"
        ]
    ]
    .sort_values("trip_distance", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\nVELOCIDADE MÉDIA - MAIORES CASOS:")

velocidade = (
    df["trip_distance"]
    / (
        (
            df["tpep_dropoff_datetime"]
            - df["tpep_pickup_datetime"]
        ).dt.total_seconds() / 3600
    )
)

resultado_velocidade = df[
    [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "fare_amount",
        "total_amount"
    ]
].copy()

resultado_velocidade["velocidade_mph"] = velocidade

print(
    resultado_velocidade
    .sort_values("velocidade_mph", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\nDURAÇÃO ZERO:")

print(
    (
        df["tpep_dropoff_datetime"]
        == df["tpep_pickup_datetime"]
    ).sum()
)