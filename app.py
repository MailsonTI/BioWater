
import streamlit as st
import pandas as pd
from database import (
    
    initialize_database,
    load_samples,
    save_samples,
    archive_and_clear_samples,
    restore_archived_samples,
    count_archived_samples,
    was_database_reset,
    get_unit_system,
    set_unit_system,
    check_database_status,
)

import hashlib
from water_analysis import analyze_water

st.set_page_config(
    page_title="BioWater",
    page_icon="💧",
    layout="wide"
)

def celsius_to_fahrenheit(value):
    return (value * 9 / 5) + 32


def fahrenheit_to_celsius(value):
    return (value - 32) * 5 / 9


def prepare_samples_for_display(data, unit_system):
    data = data.copy()

    if unit_system == "US":
        data["Temperatura (°C)"] = (
            data["Temperatura (°C)"] * 9 / 5 + 32
        )

        data.rename(
            columns={"Temperatura (°C)": "Temperatura (°F)"},
            inplace=True
        )

    if st.session_state.language == "en":

        data.rename(
            columns={
                "Local": "Location",
                "Temperatura (°C)": "Temperature (°C)",
                "Temperatura (°F)": "Temperature (°F)",
                "Oxigênio (mg/L)": "Dissolved Oxygen (mg/L)",
                "Turbidity (NTU)": "Turbidity (NTU)",
                "Conductivity (µS/cm)": "Conductivity (µS/cm)",
                "Data/Hora": "Date/Time"
            },
            inplace=True
        )

    return data

initialize_database()

st.session_state.unit_system_selector = "SI"

if "language" not in st.session_state:
    st.session_state.language = "pt"
def traduzir(portugues, ingles):
    if st.session_state.language == "pt":
        return portugues

    return ingles

# Dados demonstrativos para iniciar o projeto
dados_iniciais = pd.DataFrame([
    {
        "Local": "Sample A",
        "pH": 7.0,
        "Temperatura (°C)": 24.0,
        "Oxigênio (mg/L)": 8.1,
        "Turbidity (NTU)": None,
        "Conductivity (µS/cm)": None
    },
    {
        "Local": "Sample B",
        "pH": 6.8,
        "Temperatura (°C)": 25.5,
        "Oxigênio (mg/L)": 7.5,
        "Turbidity (NTU)": None,
        "Conductivity (µS/cm)": None
    },
    {
        "Local": "Sample C",
        "pH": 7.2,
        "Temperatura (°C)": 23.5,
        "Oxigênio (mg/L)": 8.4,
        "Turbidity (NTU)": None,
        "Conductivity (µS/cm)": None
    }
])

initialize_database()

if "amostras" not in st.session_state:
    amostras_salvas = load_samples()

    if amostras_salvas.empty and not was_database_reset():
        save_samples(dados_iniciais)
        st.session_state.amostras = load_samples()
    else:
        st.session_state.amostras = amostras_salvas

if "csv_importados" not in st.session_state:
    st.session_state.csv_importados = set()

df = st.session_state.amostras
    
# Sidebar Navigation

st.sidebar.title("💧 BioWater")

st.sidebar.divider()

st.sidebar.caption(
    traduzir(
        "Sistema de Monitoramento Ambiental",
        "Environmental Monitoring System"
    )
)

st.sidebar.radio(
    traduzir("Navegação", "Navigation"),
    [
        "Dashboard",
        "Register Samples",
        "Data History",
        "Data Management",
        "About BioWater"
    ],
    format_func=lambda pagina: {
        "Dashboard": traduzir("Painel", "Dashboard"),
        "Register Samples": traduzir("Registrar Amostras", "Register Samples"),
        "Data History": traduzir("Histórico de Dados", "Data History"),
        "Data Management": traduzir("Gerenciamento de Dados", "Data Management"),
        "About BioWater": traduzir("Sobre o BioWater", "About BioWater")
    }[pagina],
    key="navigation"
)

pagina = st.session_state.navigation

st.sidebar.divider()

col_space, col_display = st.columns([4, 1])

with col_space:
    _, col_pt, col_en = st.columns([5, 1, 1])

    with col_pt:
        flag_pt, button_pt = st.columns([1, 2])

    with flag_pt:
        st.image(
            "https://flagcdn.com/w40/br.png",
            width=32
        )

    with button_pt:
        if st.button(
            "PT",
            key="language_pt",
            type="primary" if st.session_state.language == "pt" else "secondary"
        ):
            st.session_state.language = "pt"
            st.rerun()

    with col_en:
        flag_en, button_en = st.columns([1, 2])

    with flag_en:
        st.image(
            "https://flagcdn.com/w40/us.png",
            width=32
        )

    with button_en:
        if st.button(
            "EN",
            key="language_en",
            type="primary" if st.session_state.language == "en" else "secondary"
        ):
            st.session_state.language = "en"
            st.rerun()

with col_display:
    display_mode = st.selectbox(
        "Display Mode",
        ["PC", "Mobile / Tablet"],
        index=None,
        placeholder="Automatic",
        key="display_mode"
    )

    if display_mode == "Mobile / Tablet":

        st.markdown("""
        <style>
        /* Organize columns vertically */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
            align-items: stretch !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            min-width: 0 !important;
            box-sizing: border-box !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            align-items: stretch !important;
        }

        /* Reduce lateral spacing */
        section.main > div.block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* Adjust headings */
        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

        h3 {
            font-size: 1.2rem !important;
        }

        /* Improve metric cards */
        div[data-testid="stMetric"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow-wrap: anywhere !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: clamp(1.1rem, 4vw, 1.5rem) !important;
            white-space: normal !important;
            overflow-wrap: anywhere !important;
        }

        div[data-testid="stMetricLabel"] {
            white-space: normal !important;
            overflow-wrap: anywhere !important;
        }

        /* Adapt tables */
        div[data-testid="stDataFrame"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
        }

        div[data-testid="stDataFrame"] iframe {
            max-width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="
        background: linear-gradient(120deg, #063B5C, #087E8B);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
    ">
        <h1 style="color: white; margin: 0;">
            💧 BioWater
        </h1>
        <h3 style="color: #D8F3F0; margin-top: 8px;">
            {traduzir("Sistema de Monitoramento Ambiental", "Environmental Monitoring System")}
        </h3>
        <p style="color: white; margin-bottom: 0;">
            {traduzir("Análise da Qualidade da Água e Gerenciamento de Dados Ambientais", "Water Quality Analysis and Environmental Data Management")}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
   traduzir("As medições iniciais são exemplos simulados, "
    "não observações ambientais reais.", "The initial measurements are simulated examples, "
    "not real environmental observations.", )
)

if pagina == "Dashboard":

    # Dashboard indicators
    unit_system = st.session_state.unit_system_selector

    df = prepare_samples_for_display(
        st.session_state.amostras,
        unit_system
    )

    # Translate turbidity and conductivity display columns
    if st.session_state.language == "pt":
        df.rename(
            columns={
                "Turbidity (NTU)": "Turbidez (NTU)",
                "Conductivity (µS/cm)": "Condutividade Elétrica (µS/cm)"
            },
            inplace=True
        )

    # Dynamic column names
    turbidity_column = (
        "Turbidez (NTU)"
        if st.session_state.language == "pt"
        else "Turbidity (NTU)"
    )

    conductivity_column = (
        "Condutividade Elétrica (µS/cm)"
        if st.session_state.language == "pt"
        else "Conductivity (µS/cm)"
    )

    temperature_column = (
        traduzir("Temperatura (°F)", "Temperature (°F)")
        if unit_system == "US"
        else traduzir("Temperatura (°C)", "Temperature (°C)")
    )

    oxygen_column = (
        "Dissolved Oxygen (mg/L)"
        if st.session_state.language == "en"
        else "Oxigênio (mg/L)"
    )

    location_column = (
        "Location"
        if st.session_state.language == "en"
        else "Local"
    )

    st.subheader(
        traduzir(
            "Indicadores de Desempenho Ambiental",
            "Environmental Performance Indicators"
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        traduzir("Total de Amostras", "Total Samples"),
        len(df)
    )

    col2.metric(
        traduzir("pH Médio", "Average pH"),
        f"{df['pH'].mean():.2f}" 
        if not df.empty else traduzir("N/D", "N/A")
    )

    col3.metric(
        traduzir("Oxigênio Médio", "Average Oxygen"),
        f"{df[oxygen_column].mean():.2f} mg/L"
        if not df.empty else traduzir("N/D", "N/A")
    )

    col4.metric(
        traduzir("Temperatura Média", "Average Temperature"),
        f"{df[temperature_column].mean():.2f} "
        f"{'°F' if unit_system == 'US' else '°C'}"
        if not df.empty else traduzir("N/D", "N/A")
    )

    st.divider()

    col5, col6 = st.columns(2)

    col5.metric(
        traduzir("Turbidez Média", "Average Turbidity"),
        f"{df[turbidity_column].mean():.2f} NTU"
        if df[turbidity_column].notna().any()
        else traduzir("N/D", "N/A")
    )

    col6.metric(
        traduzir("Condutividade Média", "Average Conductivity"),
        f"{df[conductivity_column].mean():.2f} µS/cm"
        if df[conductivity_column].notna().any()
        else traduzir("N/D", "N/A")
    )

    st.divider()

# Water Quality Charts

    st.header(
    traduzir(
        "Análise da Qualidade da Água",
        "Water Quality Analytics"
    )
)
    if not df.empty:

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            traduzir("Visão Geral", "Overview"),
            traduzir("Análise de pH", "pH Analysis"),
            traduzir("Análise de Temperatura", "Temperature Analysis"),
            traduzir("Análise de Oxigênio Dissolvido", "Dissolved Oxygen Analysis"),
            traduzir("Análise de Turbidez", "Turbidity Analysis"),
            traduzir("Análise de Condutividade", "Conductivity Analysis")
        ])

        with tab1:
            st.subheader(
                traduzir(
                    "Visão Geral da Qualidade da Água",
                    "Complete Water Quality Overview"
                )
            )

            grafico = df.set_index(location_column)[
                [
                    "pH",
                    temperature_column,
                    oxygen_column
                ]
            ]

            st.line_chart(grafico)

            st.caption(
                traduzir(
                    "Visualização conjunta de todos os parâmetros de qualidade da água.",
                    "Combined visualization of all water quality parameters."
                )
            )

        with tab2:
            st.subheader(
                traduzir("Medições de pH", "pH Measurements")
            )

            st.line_chart(
                df.set_index(location_column)[["pH"]]
            )

        with tab3:
            st.subheader(
                traduzir("Medições de Temperatura", "Temperature Measurements")
            )

            st.line_chart(
                df.set_index(location_column)[[temperature_column]]
            )

        with tab4:
            st.subheader(
                traduzir(
                    "Medições de Oxigênio Dissolvido",
                    "Dissolved Oxygen Measurements"
                )
            )

            st.line_chart(
                df.set_index(location_column)[[oxygen_column]]
            )

        with tab5:
            st.subheader(
                traduzir("Medições de Turbidez", "Turbidity Measurements")
            )

            st.line_chart(
                df.dropna(subset=[turbidity_column])
                .set_index(location_column)[[turbidity_column]]
            )

            st.line_chart(
                df.dropna(subset=[turbidity_column])
                .set_index(location_column)[[turbidity_column]],
                y=turbidity_column
            )

            st.caption(
                traduzir(
                    "Medições de turbidez em Unidades Nefelométricas de Turbidez (NTU).",
                    "Turbidity measurements in Nephelometric Turbidity Units (NTU)."
                )
            )

        with tab6:
            st.subheader(
                traduzir(
                    "Medições de Condutividade Elétrica",
                    "Electrical Conductivity Measurements"
                )
            )
            st.line_chart(
                df.dropna(subset=[conductivity_column])
                .set_index(location_column)[[conductivity_column]]
            )

            st.line_chart(
                df.dropna(subset=[conductivity_column])
                .set_index(location_column)[[conductivity_column]],
                y=conductivity_column
            )

            st.caption(
                traduzir(
                    "Medições de condutividade elétrica em microsiemens por centímetro (µS/cm).",
                    "Electrical conductivity measurements in microsiemens per centimeter (µS/cm)."
                )
            )

    else:
        st.info(
            traduzir(
                "Não há amostras disponíveis para visualizar os gráficos.",
                "No samples available for chart visualization."
            )
        )

    st.divider()

if pagina == "Register Samples":

    # Importação de amostras
    st.header(
        traduzir("Importar amostras de CSV", "Import samples from CSV")
    )

    st.caption(
        traduzir(
            "Tamanho máximo permitido: 200 MB por arquivo CSV.",
            "Maximum allowed size: 200 MB per CSV file."
        )
    )

    # CSV import template
    if st.session_state.language == "en":
        colunas_modelo = [
            "Location",
            "pH",
            "Temperature (°C)",
            "Dissolved Oxygen (mg/L)",
            "Turbidity (NTU)",
            "Electrical Conductivity (µS/cm)",
            "Date/Time"
        ]
        nome_arquivo = "BioWater_CSV_Template_EN.csv"

    else:
        colunas_modelo = [
            "Local",
            "pH",
            "Temperatura (°C)",
            "Oxigênio (mg/L)",
            "Turbidez (NTU)",
            "Condutividade Elétrica (µS/cm)",
            "Data/Hora"
        ]
        nome_arquivo = "Modelo_CSV_BioWater_PT.csv"

    modelo_csv = pd.DataFrame(columns=colunas_modelo)

    st.download_button(
        label=traduzir(
            "Baixar modelo CSV",
            "Download CSV Template"
        ),
        data=modelo_csv.to_csv(
            index=False,
            encoding="utf-8-sig"
        ),
        file_name=nome_arquivo,
        mime="text/csv"
    )

    with st.expander(
        traduzir("Guia de preenchimento do CSV", "CSV Filling Guide")
    ):

        st.markdown(
            traduzir(
                """
                **Orientações para preencher o arquivo:**

                - **Local:** nome do ponto de coleta.
                - **pH:** valor entre 0 e 14.
                - **Temperatura (°C):** valor entre 0 e 60.
                - **Oxigênio (mg/L):** valor entre 0 e 20.
                - **Turbidez (NTU):** valor entre 0 e 1000.
                - **Condutividade (µS/cm):** valor entre 0 e 10000.
                - **Data/Hora:** data e horário da coleta.

                **Importante:** utilize números nas medições e não altere os nomes das colunas do modelo.
                """,
                """
                **Instructions for filling out the file:**

                - **Location:** name of the sampling point.
                - **pH:** value between 0 and 14.
                - **Temperature (°C):** value between 0 and 60.
                - **Dissolved Oxygen (mg/L):** value between 0 and 20.
                - **Turbidity (NTU):** value between 0 and 1000.
                - **Electrical Conductivity (µS/cm):** value between 0 and 10000.
                - **Date/Time:** sampling date and time.

                **Important:** use numbers for measurements and do not change the template column names.
                """
            )
        )

    arquivo_csv = st.file_uploader(
        traduzir("Selecionar arquivo CSV", "Select CSV file"),
        type=["csv"],
        help=traduzir(
            "Envie um arquivo CSV contendo medições da qualidade da água.",
            "Upload a CSV file containing water quality measurements."
        )
    )

    st.caption(
        traduzir(
            "Envie um arquivo CSV para importar várias amostras de água de uma só vez.",
            "Upload a CSV file to import multiple water quality samples at once."
        )
    )

    if arquivo_csv is not None:
        dados_csv = pd.read_csv(arquivo_csv)

        # Normalize English CSV headers to the internal Portuguese names
        mapa_colunas_csv = {
            # Location
            "Location": "Local",
            "location": "Local",
            "Sample Location": "Local",
            "Local": "Local",
            "local": "Local",

            # pH
            "Ph": "pH",
            "PH": "pH",

            # Temperature
            "Temperature (°C)": "Temperatura (°C)",
            "Temperature (C)": "Temperatura (°C)",
            "temperatura (°C)": "Temperatura (°C)",
            "Temperatura": "Temperatura (°C)",

            "Temperature (°F)": "Temperatura (°F)",
            "Temperature (F)": "Temperatura (°F)",

            # Dissolved oxygen
            "Dissolved Oxygen (mg/L)": "Oxigênio (mg/L)",
            "Oxygen (mg/L)": "Oxigênio (mg/L)",
            "Oxigenio (mg/L)": "Oxigênio (mg/L)",

            # Turbidity
            "Turbidity": "Turbidity (NTU)",
            "Turbidity (NTU)": "Turbidity (NTU)",
            "Turbidez": "Turbidity (NTU)",

            # Conductivity
            "Conductivity": "Conductivity (µS/cm)",
            "Electrical Conductivity (µS/cm)": "Conductivity (µS/cm)",
            "Condutividade": "Conductivity (µS/cm)",
            "Condutividade Elétrica (µS/cm)": "Conductivity (µS/cm)",

            # Date and time
            "Date/Time": "Data/Hora",
            "Date": "Data/Hora",
            "Data": "Data/Hora"
        }

        dados_csv.rename(
            columns=mapa_colunas_csv,
            inplace=True
        )    

         # Check for duplicate column names after normalization
        if dados_csv.columns.duplicated().any():
            st.error(
                traduzir(
                    "O arquivo CSV contém colunas duplicadas ou incompatíveis.",
                    "The CSV file contains duplicate or conflicting columns."
                ),
                icon="❌"
            )
            st.stop()
                        
        # Convert US temperature to Celsius when necessary
        if (
                "Temperatura (°F)" in dados_csv.columns
                and "Temperatura (°C)" not in dados_csv.columns
            ):
            dados_csv["Temperatura (°C)"] = (
                pd.to_numeric(
                    dados_csv["Temperatura (°F)"],
                    errors="coerce"
                ) - 32
            ) * 5 / 9

            dados_csv["Temperatura (°C)"] = (
                dados_csv["Temperatura (°C)"].round(2)
            )

            dados_csv.drop(
                columns=["Temperatura (°F)"],
                inplace=True
            )

        assinatura = hashlib.sha256(
            arquivo_csv.getvalue()
        ).hexdigest()

        # Required columns (compatible with older CSV files)
        colunas_obrigatorias = [
            "Local",
            "pH",
            "Temperatura (°C)",
            "Oxigênio (mg/L)"
        ]

        colunas_faltando = [
            coluna
            for coluna in colunas_obrigatorias
            if coluna not in dados_csv.columns
        ]

        # Optional columns
        colunas_opcionais = [
            "Turbidity (NTU)",
            "Conductivity (µS/cm)"
        ]

        if not colunas_faltando:
            for coluna in colunas_opcionais:
                if coluna not in dados_csv.columns:
                    dados_csv[coluna] = None

            if "Data/Hora" not in dados_csv.columns:
                dados_csv["Data/Hora"] = None

            # Organize CSV columns
            colunas_ordenadas = [
                "Local",
                "pH",
                "Temperatura (°C)",
                "Oxigênio (mg/L)",
                "Turbidity (NTU)",
                "Conductivity (µS/cm)",
                "Data/Hora"
            ]

            outras_colunas = [
                coluna
                for coluna in dados_csv.columns
                if coluna not in colunas_ordenadas
            ]

            dados_csv = dados_csv[
                [
                    coluna
                    for coluna in colunas_ordenadas
                    if coluna in dados_csv.columns
                ] + outras_colunas
            ]

            dados_csv["Local"] = (
                dados_csv["Local"]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            colunas_numericas = [
                "pH",
                "Temperatura (°C)",
                "Oxigênio (mg/L)"
            ] + colunas_opcionais

            valores_numericos_originais = dados_csv[
                colunas_numericas
            ].copy()

            for coluna in colunas_numericas:
                dados_csv[coluna] = pd.to_numeric(
                    dados_csv[coluna],
                    errors="coerce"
                )

            local_vazio = dados_csv["Local"].eq("").any()

            linhas_numeros_invalidos = set()

            for coluna in [
                "pH",
                "Temperatura (°C)",
                "Oxigênio (mg/L)"
            ]:
                linhas_numeros_invalidos.update(
                    dados_csv.index[dados_csv[coluna].isna()]
                )

            for coluna in colunas_opcionais:
                valor_original = valores_numericos_originais[coluna]
                campo_preenchido = (
                    valor_original.notna()
                    & valor_original.astype(str).str.strip().ne("")
                )
                valor_convertido_invalido = (
                    campo_preenchido & dados_csv[coluna].isna()
                )
                linhas_numeros_invalidos.update(
                    dados_csv.index[valor_convertido_invalido]
                )

            numero_invalido = bool(linhas_numeros_invalidos)
            linhas_csv_com_numeros_invalidos = sorted(
                indice + 2 for indice in linhas_numeros_invalidos
            )

            fora_dos_limites = (
                (~dados_csv["pH"].between(0, 14)).any()
                or (~dados_csv["Temperatura (°C)"].between(0, 60)).any()
                or (~dados_csv["Oxigênio (mg/L)"].between(0, 20)).any()
                or (
                    dados_csv["Turbidity (NTU)"].notna()
                    & ~dados_csv["Turbidity (NTU)"].between(0, 1000)
                ).any()
                or (
                    dados_csv["Conductivity (µS/cm)"].notna()
                    & ~dados_csv["Conductivity (µS/cm)"].between(0, 10000)
                ).any()
            )

        if colunas_faltando:
            st.error(
                traduzir(
                    "O CSV não contém estas colunas obrigatórias: ",
                    "CSV is missing these required columns: "
                ) + ", ".join(colunas_faltando),
                icon="❌"
            )

        elif dados_csv.empty:
            st.error(
                traduzir(
                    "O arquivo CSV não contém registros de amostras.",
                    "The CSV file contains no sample records."
                ),
                icon="❌"
            )

        elif local_vazio:
            st.error(
                traduzir(
                    "Todas as amostras devem ter um local informado.",
                    "Every sample must have a location."
                ),
                icon="❌"
            )

        elif numero_invalido:
            st.error(
                traduzir(
                    "Números inválidos nas linhas do CSV (contando o cabeçalho): "
                    + ", ".join(map(str, linhas_csv_com_numeros_invalidos))
                    + ". Corrija os valores ou deixe os campos opcionais em branco.",
                    "Invalid numbers on CSV lines (including the header): "
                    + ", ".join(map(str, linhas_csv_com_numeros_invalidos))
                    + ". Correct the values or leave optional fields blank."
                ),
                icon="❌"
            )

        elif fora_dos_limites:
            st.error(
                traduzir(
                    "Uma ou mais medições estão fora dos limites permitidos.",
                    "One or more measurements are outside the allowed range."
                ),
                icon="❌"
            )

        elif assinatura in st.session_state.csv_importados:
            st.warning(
                traduzir(
                    "Este arquivo CSV já foi importado.",
                    "This CSV file has already been imported."
                ),
                icon="⚠️"
            )

        else:
            st.subheader(
                traduzir("Pré-visualização da Importação", "Import Preview")
            )

            st.caption(
                traduzir(
                    f"Revise as {len(dados_csv)} amostras antes de importar.",
                    f"Review the {len(dados_csv)} samples before importing."
                )
            )

            dados_csv_exibicao = dados_csv.copy()

            if st.session_state.language == "en":
                dados_csv_exibicao.rename(
                    columns={
                        "Local": "Location",
                        "Temperatura (°C)": "Temperature (°C)",
                        "Temperatura (°F)": "Temperature (°F)",
                        "Oxigênio (mg/L)": "Dissolved Oxygen (mg/L)",
                        "Data/Hora": "Date/Time"
                    },
                    inplace=True
                )

            st.dataframe(
                dados_csv_exibicao,
                width="stretch",
                hide_index=True
            )

            if st.button(
                traduzir("Importar Amostras", "Import Samples"),
                type="primary"
            ):
                save_samples(dados_csv)

                st.session_state.amostras = pd.concat(
                    [st.session_state.amostras, dados_csv],
                    ignore_index=True
                )

                st.session_state.csv_importados.add(assinatura)

                st.success(
                    traduzir(
                        f"{len(dados_csv)} amostras importadas com sucesso!",
                        f"Successfully imported {len(dados_csv)} samples!"
                    ),
                    icon="✅"
                )
                st.rerun()
                
        
    # Manual sample registration
    st.divider()
    st.header(
        traduzir("Registro Manual de Amostras", "Manual Sample Registration"
                 )
        )

    with st.form("sample_form"):

        local = st.text_input(traduzir("Local da amostra", "Sample location"))

        col1, col2 = st.columns(2)

        with col1:
            ph = st.number_input(
                traduzir("pH", "pH"),
                min_value=0.0,
                max_value=14.0,
                value=7.0,
                step=0.1
            )

        with col2:
            unit_system = st.session_state.unit_system_selector

            if unit_system == "US":
                temperatura_input = st.number_input(
                    traduzir("Temperatura (°F)", "Temperature (°F)"),
                    min_value=32.0,
                    max_value=140.0,
                    value=77.0,
                    step=1.0
                )

                temperatura_c = fahrenheit_to_celsius(
                    temperatura_input
                )

            else:
                temperatura_input = st.number_input(
                    traduzir("Temperatura (°C)", "Temperature (°C)"),
                    min_value=0.0,
                    max_value=60.0,
                    value=25.0,
                    step=0.5
                )

                temperatura_c = temperatura_input

        col3, col4 = st.columns(2)

        with col3:
            oxigenio = st.number_input(
                traduzir("Oxigênio (mg/L)", "Dissolved oxygen (mg/L)"),
                min_value=0.0,
                max_value=20.0,
                value=8.0,
                step=0.1
            )

        with col4:
            turbidez = st.number_input(
                traduzir("Turbidez (NTU)", "Turbidity (NTU)"),
                min_value=0.0,
                max_value=1000.0,
                value=1.0,
                step=0.1
            )

        condutividade = st.number_input(
            traduzir("Condutividade Elétrica (µS/cm)", "Electrical Conductivity (µS/cm)"),
            min_value=0.0,
            max_value=10000.0,
            value=100.0,
            step=1.0
        )

        enviar = st.form_submit_button(
            traduzir("Registrar", "Register Sample"),
            type="primary"
        )


    if enviar:
        if not local.strip():
            st.warning(
                traduzir(
                    "Informe o local da amostra.",
                    "Please enter a sample location."
                ),
                icon="⚠️"
            )
        else:
            nova_amostra = pd.DataFrame([{
                "Local": local.strip(),
                "pH": ph,
                "Temperatura (°C)": temperatura_c,
                "Oxigênio (mg/L)": oxigenio,
                "Turbidity (NTU)": turbidez,
                "Conductivity (µS/cm)": condutividade
            }])

            save_samples(nova_amostra)

            st.session_state.amostras = pd.concat(
                [st.session_state.amostras, nova_amostra],
                ignore_index=True
            )

            st.success(
                traduzir(
                    "Amostra de água registrada com sucesso!",
                    "Water sample registered successfully!"
                ),
                icon="✅"
            )

            st.subheader(traduzir("Análise da Qualidade da Água", "Water Quality Analysis"))

            st.caption(
                traduzir("Análise dos parâmetros de qualidade da água registrados.","Assessment of the recorded water quality parameters.")
            )

            st.info(
                traduzir(
                    "A classificação apresentada utiliza critérios simplificados de referência para fins informativos. "
                    "Ela não representa uma certificação de potabilidade nem substitui análises laboratoriais "
                    "ou a avaliação conforme as normas aplicáveis.",
                    "The displayed classification uses simplified reference criteria for informational purposes. "
                    "It does not certify drinking water safety or replace laboratory testing "
                    "or assessment under applicable standards."
                )
            )

            resultados = analyze_water(
                ph,
                temperatura_c,
                oxigenio,
                turbidez,
                condutividade,
                st.session_state.language
            )
            
            st.divider()

            
            for resultado in resultados:

                mensagem = (
                    f'{resultado["parameter"]}: '
                    f'{resultado["value"]} — {resultado["status"]}'
                )

                if resultado["color"] == "green":
                    st.success(mensagem, icon="✅")

                elif resultado["color"] == "blue":
                    st.info(mensagem, icon="ℹ️")

                else:
                    st.error(mensagem, icon="⚠️")
                  

if pagina == "Data History":

    # Historical records
    st.header(
        traduzir(
            "Histórico de Monitoramento Ambiental",
            "Environmental Monitoring History"
        )
    )

    st.write(
        traduzir(
            "Histórico Completo das Amostras de Água Registradas.",
            "Complete history of registered water samples."
        )
    )

    historico = load_samples()

    historico_exibicao = prepare_samples_for_display(
        historico,
        st.session_state.unit_system_selector
    )

    # Translate display columns in Portuguese
    if st.session_state.language == "pt":
        historico_exibicao.rename(
            columns={
                "Turbidity (NTU)": "Turbidez (NTU)",
                "Conductivity (µS/cm)": "Condutividade Elétrica (µS/cm)"
            },
            inplace=True
        )

    st.dataframe(
        historico_exibicao,
        width="stretch",
        height=500,
        hide_index=True,

                column_order=[
            traduzir("Local", "Location"),
            "pH",
            traduzir(
                "Temperatura (°F)",
                "Temperature (°F)"
            )
            if st.session_state.unit_system_selector == "US"
            else traduzir(
                "Temperatura (°C)",
                "Temperature (°C)"
            ),
            traduzir(
                "Oxigênio (mg/L)",
                "Dissolved Oxygen (mg/L)"
            ),
            traduzir("Turbidez (NTU)", "Turbidity (NTU)"),
            traduzir(
                "Condutividade Elétrica (µS/cm)",
                "Conductivity (µS/cm)"
            ),
            traduzir("Data/Hora", "Date/Time")
        ],
        column_config={
            traduzir("Local", "Location"): st.column_config.TextColumn(
                traduzir("Local", "Location"),
                pinned=True
            )
        }
    )

    csv = historico_exibicao.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.divider()

    nome_arquivo = (
        "historico_biowater_pt.csv"
        if st.session_state.language == "pt"
        else "biowater_history_en.csv"
    )

    st.download_button(
        label=traduzir("Baixar CSV", "Download CSV"),
        data=csv,
        file_name=nome_arquivo,
        mime="text/csv"
    )


if pagina == "Data Management":

    # DATA MANAGEMENT
    st.divider()

    st.header(
        traduzir("Gerenciamento de Dados", "Data Management")
    )

    database_ok = check_database_status()
    
    if "reset_success_message" in st.session_state:
        st.success(st.session_state.pop("reset_success_message"))

    if "restore_success_message" in st.session_state:
        st.success(st.session_state.pop("restore_success_message"))

        st.write(
            traduzir(
                "Gerencie seus registros de monitoramento ambiental "
                "e recupere amostras arquivadas.",
                "Manage your environmental monitoring records "
                "and recover archived samples."
            )
        )
        
    total_arquivadas = count_archived_samples()
    reset_realizado = was_database_reset()
    total_amostras = len(st.session_state.amostras)

    # DATABASE OVERVIEW
    st.subheader(
        traduzir("Visão Geral da Base de Dados", "Database Overview")
    )

    st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.20);
        padding: 16px;
        border-radius: 12px;
        height: 105px;
        }
    </style>
    """, unsafe_allow_html=True)

    col_status, col_active, col_archived, col_type = st.columns(
    [1, 1, 1, 1]
    )

    with col_status:
        status_color = "#16A34A" if database_ok else "#DC2626"
        status_value = (
            traduzir("OK", "OK")
            if database_ok
            else traduzir("Erro", "Error")
        )

        st.markdown(
            f"""
            <div style="
                background-color: rgba(128, 128, 128, 0.08);
                border: 1px solid rgba(128, 128, 128, 0.20);
                padding: 16px;
                border-radius: 12px;
                min-height: 105px;
            ">
            <div style="
                font-size: 14px;
                margin-bottom: 8px;
            ">
                {traduzir("Status do Banco de Dados", "Database Status")}
            </div>
            <div style="
                font-size: 28px;
                font-weight: 600;
                color: {status_color};
            ">
                {status_value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col_active:
        st.metric(
            traduzir("Amostras Ativas", "Active Samples"),
            total_amostras
        )

    with col_archived:
        st.metric(
            traduzir("Amostras Arquivadas", "Archived Samples"),
            total_arquivadas
        )

    with col_type:
        st.metric(
            traduzir("Tipo de Banco de Dados", "Database Type"),
            "SQLite"
        )

    # DATABASE OPERATIONS
    st.divider()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader(
            traduzir("Resetar Base de Dados", "Reset Database")
        )

        st.write(
            traduzir(
                f"Você está prestes a arquivar {total_amostras} amostras. "
                "Elas sairão da lista ativa, mas permanecerão armazenadas "
                "e poderão ser restauradas posteriormente.",
                f"You are about to archive {total_amostras} samples. "
                "They will leave the active list but remain stored "
                "and can be restored later."
            )
        )

        confirmar = st.checkbox(
            traduzir(
                "Confirmo que desejo redefinir o banco de dados.",
                "I confirm that I want to reset the database."
            ),
            key="confirm_reset"
        )

        if st.button(
            traduzir("Redefinir amostras", "Reset samples"
                     ),
            disabled=(not confirmar or total_amostras == 0)
        ):

            try:
                archive_and_clear_samples()

                st.session_state.amostras = load_samples()
                st.session_state.csv_importados = set()

                st.session_state["reset_success_message"] = traduzir(
                    "Banco de dados redefinido com sucesso. "
                    "As amostras anteriores foram arquivadas.",
                    "Database reset successfully. "
                    "Previous samples were archived."
                )

                st.rerun()

            except Exception as error:
                st.error(
                    traduzir(
                        f"Falha ao redefinir o banco de dados. "
                        f"Suas amostras ativas foram preservadas. Erro: {error}",
                        f"Database reset failed. "
                        f"Your active samples were preserved. Error: {error}"
                    )
                )

    
    
    with col2:

        if reset_realizado and total_arquivadas > 0:

            st.subheader(
                traduzir("Recuperar Amostras", "Recover Samples")
            )

            st.write(
                traduzir(
                    f"Amostras arquivadas disponíveis: {total_arquivadas}",
                    f"Archived samples available: {total_arquivadas}"
                )
            )

            if st.button(
                traduzir("Restaurar amostras arquivadas", "Restore archived samples"
                         )
            ):

                try:
                    restored_count = restore_archived_samples()

                    st.session_state.amostras = load_samples()

                    st.session_state["restore_success_message"] = traduzir(
                        f"{restored_count} amostras restauradas com sucesso!",
                        f"{restored_count} samples restored successfully!"
                    )

                    st.rerun()

                except Exception as error:
                    st.error(
                        traduzir(
                            f"Falha ao restaurar as amostras: {error}",
                            f"Sample restoration failed: {error}"
                        )
                    )

if pagina == "About BioWater":
    
    with st.container(border=True):

        col1, col2 = st.columns([3, 1])

        with col1:
            st.caption(
                traduzir("TECNOLOGIA AMBIENTAL", "ENVIRONMENTAL TECHNOLOGY")
            )

            st.title("💧 BioWater")

            st.subheader(
                traduzir("Ciência Sem Fronteiras", "Science Without Borders")
            )

        with col2:
            st.markdown(
                """
                <div style="text-align: center; font-size: 28px;">
                    🇧🇷 ⇄ 🇺🇸
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                traduzir(
                    "DO BRASIL PARA O MUNDO", "BRAZIL TO THE WORLD"
                    )
            )

        st.divider()

        st.write(
            traduzir(
                "Desenvolvido no Brasil. Construído com padrões globais de tecnologia.",
                "Developed in Brazil. Built with global technology standards."
            )
        )

        st.write(
            traduzir(
                "Conectando a Ciência Ambiental e o Desenvolvimento de Software.",
                "Connecting Environmental Science and Software Development."
            )
        )

    st.subheader(
        traduzir("Sobre o Projeto", "About the Project")
    )

    st.write(
        traduzir(
            "O BioWater é uma aplicação de monitoramento ambiental e análise "
            "da qualidade da água, desenvolvida para integrar Ciências Ambientais "
            "e Tecnologia da Informação por meio de ferramentas digitais.",
            "BioWater is an environmental monitoring and water quality analysis "
            "application designed to integrate Environmental Science and "
            "Information Technology through digital tools."
        )
    )

    st.divider()

    st.subheader(
        traduzir("Recursos Principais", "Core Features")
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader(
                traduzir("🧪 Análise da Água", "🧪 Water Analysis")
            )
            st.write(
                traduzir(
                    "Medições da qualidade da água e análise automática.",
                    "Water quality measurements and automatic analysis."
                )
            )

        with st.container(border=True):
            st.subheader(
                traduzir("📊 Análise Ambiental", "📊 Environmental Analytics")
            )
            st.write(
                traduzir(
                    "Gráficos interativos e indicadores ambientais.",
                    "Interactive charts and environmental indicators."
                )
            )

    with col2:
        with st.container(border=True):
            st.subheader(
                traduzir("🗄️ Gerenciamento de Dados", "🗄️ Data Management")
            )
            st.write(
                traduzir(
                    "Banco de dados SQLite, histórico de amostras e integração CSV.",
                    "SQLite database, sample history and CSV integration."
                )
            )

        with st.container(border=True):
            st.subheader(
                traduzir("🌎 Tecnologia Global", "🌎 Global Technology")
            )
            st.write(
                traduzir(
                    "Conectando Ciências Ambientais e desenvolvimento de software.",
                    "Connecting environmental science and software development."
                )
            )

    st.markdown(
        traduzir(
            """
            - Registro de dados da qualidade da água
            - Importação e exportação de dados CSV
            - Análise automática da qualidade da água
            - Painéis ambientais interativos
            - Integração com banco de dados SQLite
            - Gerenciamento de dados históricos
            """,
            """
            - Water quality data registration
            - CSV data import and export
            - Automatic water quality analysis
            - Interactive environmental dashboards
            - SQLite database integration
            - Historical data management
            """
        )
    )

    st.divider()

    st.subheader(
        traduzir("Tecnologias Utilizadas", "Technologies Used")
    )

    tech1, tech2, tech3 = st.columns(3)

    with tech1:
        st.info(
            traduzir(
                "🐍 Python\n\nPrincipal linguagem de programação",
                "🐍 Python\n\nMain programming language"
            )
        )

    with tech2:
        st.info(
            traduzir(
                "⚡ Streamlit\n\nAplicação web interativa",
                "⚡ Streamlit\n\nInteractive web application"
            )
        )

    with tech3:
        st.info(
            traduzir(
                "📊 Pandas\n\nProcessamento e análise de dados",
                "📊 Pandas\n\nData processing and analysis"
            )
        )

    tech4, tech5 = st.columns(2)

    with tech4:
        st.info(
            traduzir(
                "🗄️ SQLite\n\nGerenciamento de banco de dados",
                "🗄️ SQLite\n\nDatabase management"
            )
        )

    with tech5:
        st.info(
            traduzir(
                "🔗 Git e GitHub\n\nControle de versão e hospedagem do projeto",
                "🔗 Git and GitHub\n\nVersion control and project hosting"
            )
        )

    st.divider()

    st.subheader(
        traduzir("Desenvolvedor do Projeto", "Project Developer")
    )

    st.info(
        traduzir(
            """
            **Mailson Maciel de Freitas**

            Desenvolvedor Python | Ciência e Tecnologia Ambiental

            Biologia | Análise e Desenvolvimento de Sistemas

            Tecnologia Ambiental
            """,

            """
            **Mailson Maciel de Freitas**

            Python Developer | Environmental Science & Technology

            Biology | Systems Analysis and Development

            Environmental Technology
            """
        )
    )

    st.caption(
        traduzir(
            "BioWater — Ciência Sem Fronteiras | Tecnologia Ambiental.",
            "BioWater — Science Without Borders | Environmental Technology."
        )
    )
