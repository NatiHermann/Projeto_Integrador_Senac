from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from pipeline import CONFIG_PATH, load_config, run_pipeline


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

            :root {
                --bg-main: #f6efe5;
                --bg-card: rgba(255, 255, 255, 0.82);
                --text-main: #123b7a;
                --accent: #ec6d0b;
                --accent-soft: #ffd9b8;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(236, 109, 11, 0.14), transparent 28%),
                    radial-gradient(circle at top right, rgba(18, 59, 122, 0.18), transparent 32%),
                    linear-gradient(180deg, #fffaf4 0%, var(--bg-main) 100%);
                color: var(--text-main);
                font-family: 'Space Grotesk', sans-serif;
            }

            .hero {
                padding: 1.6rem 1.8rem;
                border-radius: 24px;
                background: linear-gradient(135deg, rgba(18,59,122,0.96), rgba(23,88,165,0.86));
                color: white;
                box-shadow: 0 24px 60px rgba(18, 59, 122, 0.18);
                margin-bottom: 1.2rem;
            }

            .hero h1, .hero p {
                color: white;
                margin: 0;
            }

            .hero p {
                margin-top: 0.5rem;
                opacity: 0.92;
            }

            [data-testid="stMetric"] {
                background: var(--bg-card);
                border: 1px solid rgba(18, 59, 122, 0.08);
                padding: 0.8rem;
                border-radius: 18px;
                box-shadow: 0 14px 32px rgba(18, 59, 122, 0.08);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #123b7a 0%, #0d2c59 100%);
            }

            [data-testid="stSidebar"] * {
                color: #ffffff;
            }

            .caption-box {
                padding: 1rem 1.2rem;
                border-radius: 18px;
                background: rgba(236, 109, 11, 0.08);
                border: 1px solid rgba(236, 109, 11, 0.16);
                margin-bottom: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_table(database_path: str, table_name: str) -> pd.DataFrame:
    with sqlite3.connect(database_path) as connection:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


def format_number(value: float) -> str:
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}".replace(",", ".")


def format_decimal(value: float) -> str:
    if pd.isna(value):
        return "0,00"
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def show_dashboard(database_path: str, tables: dict) -> None:
    curated = load_table(database_path, tables["curated"])
    summary = load_table(database_path, tables["summary"])

    curated["data_extracao"] = pd.to_datetime(curated["data_extracao"], errors="coerce")

    st.markdown(
        """
        <div class="hero">
            <h1>Painel Low Code do Projeto Integrador</h1>
            <p>ETL em pandas, carga em SQLite e visualizacao interativa sobre o arquivo base do Kaggle.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="caption-box">
            O pipeline transforma o CSV de metadados do Onco360, padroniza tipos, gera indicadores derivados e salva a base tratada para analise.
        </div>
        """,
        unsafe_allow_html=True,
    )

    formatos = sorted(curated["formato"].dropna().unique().tolist())
    portes = sorted(curated["porte_arquivo"].dropna().unique().tolist())

    col_filter_1, col_filter_2 = st.columns(2)
    with col_filter_1:
        formato_selecionado = st.multiselect("Filtrar por formato", formatos, default=formatos)
    with col_filter_2:
        porte_selecionado = st.multiselect("Filtrar por porte do arquivo", portes, default=portes)

    filtered = curated[curated["formato"].isin(formato_selecionado) & curated["porte_arquivo"].isin(porte_selecionado)]

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Arquivos no painel", format_number(filtered["arquivo"].count()))
    metric_2.metric("Total de registros", format_number(filtered["numero_registros"].sum()))
    metric_3.metric("Tamanho total MiB", format_decimal(filtered["tamanho_mib"].sum()))
    metric_4.metric(
        "Ultima extracao",
        filtered["data_extracao"].max().strftime("%d/%m/%Y") if not filtered.empty and filtered["data_extracao"].notna().any() else "N/D",
    )

    chart_col_1, chart_col_2 = st.columns(2)

    with chart_col_1:
        top_files = filtered.nlargest(10, "numero_registros")
        fig_bar = px.bar(
            top_files,
            x="numero_registros",
            y="arquivo",
            orientation="h",
            color="porte_arquivo",
            color_discrete_sequence=["#123b7a", "#ec6d0b", "#ffa94d", "#1f6fd5"],
            title="Top 10 arquivos por volume de registros",
        )
        fig_bar.update_layout(height=420, yaxis_title="", xaxis_title="Registros")
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col_2:
        fig_scatter = px.scatter(
            filtered,
            x="tamanho_mib",
            y="numero_registros",
            color="formato",
            size="registros_por_mib",
            hover_name="arquivo",
            title="Relacao entre tamanho do arquivo e quantidade de registros",
            color_discrete_sequence=["#ec6d0b", "#123b7a", "#4a90e2"],
        )
        fig_scatter.update_layout(height=420, xaxis_title="Tamanho MiB", yaxis_title="Registros")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Resumo agregado")
    st.dataframe(summary, width="stretch", hide_index=True)

    st.subheader("Base tratada")
    st.dataframe(
        filtered.sort_values(by="numero_registros", ascending=False),
        width="stretch",
        hide_index=True,
    )


def main() -> None:
    st.set_page_config(page_title="Projeto Integrador Senac", layout="wide")
    inject_styles()

    config = load_config(CONFIG_PATH)
    st.sidebar.title("Configurar ETL")
    source_path = st.sidebar.text_input("Arquivo base CSV", value=config["source_csv"])
    st.sidebar.caption("Altere o caminho se quiser usar outro arquivo CSV com a mesma estrutura.")

    database_path = config["database_path"]
    database_exists = Path(database_path).exists()

    if not database_exists:
        with st.spinner("Primeira execucao detectada. Gerando banco de dados..."):
            result = run_pipeline(CONFIG_PATH, source_path=source_path)
        st.sidebar.success(f"ETL concluido: {result['rows_loaded']} linhas carregadas.")
        database_path = result["database_path"]
        database_exists = True

    if st.sidebar.button("Executar ETL"):
        with st.spinner("Processando arquivo e atualizando o banco SQLite..."):
            result = run_pipeline(CONFIG_PATH, source_path=source_path)
        st.sidebar.success(f"ETL concluido: {result['rows_loaded']} linhas carregadas.")
        database_path = result["database_path"]
        database_exists = True

    show_dashboard(database_path, config["tables"])


if __name__ == "__main__":
    main()
