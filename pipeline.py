from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config" / "project.yaml"


def load_config(config_path: Path | None = None) -> dict:
    path = config_path or CONFIG_PATH
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    config["source_csv"] = str(Path(config["source_csv"]).expanduser())
    config["database_path"] = str((PROJECT_ROOT / config["database_path"]).resolve())
    config["processed_csv_path"] = str((PROJECT_ROOT / config["processed_csv_path"]).resolve())
    return config


def extract_data(source_path: str) -> pd.DataFrame:
    csv_path = Path(source_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo de origem nao encontrado: {csv_path}")
    return pd.read_csv(csv_path)


def classify_size(size_mib: float) -> str:
    if pd.isna(size_mib):
        return "nao_informado"
    if size_mib < 1:
        return "muito_pequeno"
    if size_mib < 100:
        return "pequeno"
    if size_mib < 500:
        return "medio"
    return "grande"


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    curated = df.copy()
    curated.columns = [
        "data_extracao",
        "arquivo",
        "numero_registros",
        "tamanho_mib",
    ]

    curated["data_extracao"] = pd.to_datetime(curated["data_extracao"], errors="coerce")
    curated["numero_registros"] = pd.to_numeric(curated["numero_registros"], errors="coerce")
    curated["tamanho_mib"] = pd.to_numeric(curated["tamanho_mib"], errors="coerce")

    curated["nome_base"] = curated["arquivo"].str.replace(r"\.[^.]+$", "", regex=True)
    curated["camada"] = curated["nome_base"].str.extract(r"^(raw|silver|gold)", expand=False).fillna("raw")
    curated["dominio"] = curated["nome_base"].str.replace(r"^(raw|silver|gold)_", "", regex=True)
    curated["formato"] = curated["arquivo"].str.extract(r"(\.[^.]+)$", expand=False).fillna("desconhecido")
    curated["porte_arquivo"] = curated["tamanho_mib"].apply(classify_size)
    curated["registros_por_mib"] = (curated["numero_registros"] / curated["tamanho_mib"]).round(2)
    curated["ano_extracao"] = curated["data_extracao"].dt.year
    curated["mes_extracao"] = curated["data_extracao"].dt.month
    curated["data_extracao"] = curated["data_extracao"].dt.strftime("%Y-%m-%d %H:%M:%S")

    curated = curated.sort_values(by="numero_registros", ascending=False).reset_index(drop=True)
    return curated


def build_summary(curated: pd.DataFrame) -> pd.DataFrame:
    summary = (
        curated.groupby(["formato", "porte_arquivo"], dropna=False)
        .agg(
            quantidade_arquivos=("arquivo", "count"),
            total_registros=("numero_registros", "sum"),
            total_tamanho_mib=("tamanho_mib", "sum"),
            media_registros_por_mib=("registros_por_mib", "mean"),
        )
        .reset_index()
    )
    summary["media_registros_por_mib"] = summary["media_registros_por_mib"].round(2)
    summary["total_tamanho_mib"] = summary["total_tamanho_mib"].round(2)
    return summary


def load_data(curated: pd.DataFrame, summary: pd.DataFrame, database_path: str, processed_csv_path: str, tables: dict) -> None:
    db_path = Path(database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    Path(processed_csv_path).parent.mkdir(parents=True, exist_ok=True)

    curated.to_csv(processed_csv_path, index=False)

    with sqlite3.connect(db_path) as connection:
        curated.to_sql(tables["curated"], connection, if_exists="replace", index=False)
        summary.to_sql(tables["summary"], connection, if_exists="replace", index=False)


def run_pipeline(config_path: Path | None = None, source_path: str | None = None) -> dict:
    config = load_config(config_path)
    if source_path:
        config["source_csv"] = str(Path(source_path).expanduser())

    raw_df = extract_data(config["source_csv"])
    curated = transform_data(raw_df)
    summary = build_summary(curated)
    load_data(
        curated=curated,
        summary=summary,
        database_path=config["database_path"],
        processed_csv_path=config["processed_csv_path"],
        tables=config["tables"],
    )

    return {
        "source_csv": config["source_csv"],
        "database_path": config["database_path"],
        "processed_csv_path": config["processed_csv_path"],
        "rows_loaded": int(len(curated)),
        "total_registros": int(curated["numero_registros"].sum()),
        "total_tamanho_mib": float(curated["tamanho_mib"].sum()),
    }


if __name__ == "__main__":
    result = run_pipeline()
    print("ETL concluido com sucesso")
    print(result)
