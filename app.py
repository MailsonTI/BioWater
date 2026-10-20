
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="BioWater",
    page_icon="💧",
    layout="wide"
)

# Dados demonstrativos para iniciar o projeto
dados_iniciais = pd.DataFrame([
    {
        "Local": "Sample A",
        "pH": 7.0,
        "Temperatura (°C)": 24.0,
        "Oxigênio (mg/L)": 8.1
    },
    {
        "Local": "Sample B",
        "pH": 6.8,
        "Temperatura (°C)": 25.5,
        "Oxigênio (mg/L)": 7.5
    },
    {
        "Local": "Sample C",
        "pH": 7.2,
        "Temperatura (°C)": 23.5,
        "Oxigênio (mg/L)": 8.4
    }
])

if "amostras" not in st.session_state:
    st.session_state.amostras = dados_iniciais.copy()

st.title("BioWater")
st.subheader("Environmental Monitoring System")
st.write(
    "An educational dashboard for water quality data."
)

st.info(
    "The initial measurements are simulated examples, "
    "not real environmental observations."
)

# Indicadores
df = st.session_state.amostras

col1, col2, col3 = st.columns(3)

col1.metric("Total samples", len(df))
col2.metric("Average pH", f"{df['pH'].mean():.2f}")
col3.metric(
    "Average oxygen",
    f"{df['Oxigênio (mg/L)'].mean():.2f} mg/L"
)

st.divider()

# Gráfico
st.header("Water Quality Overview")

grafico = df.set_index("Local")[
    ["pH", "Temperatura (°C)", "Oxigênio (mg/L)"]
]

st.line_chart(grafico)

st.caption(
    "The chart uses different measurement units. "
    "Compare each variable separately."
)

# Cadastro de amostras
st.header("Register a Water Sample")

with st.form("sample_form"):
    local = st.text_input("Sample location")

    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1
    )

    temperatura = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=60.0,
        value=25.0,
        step=0.5
    )

    oxigenio = st.number_input(
        "Dissolved oxygen (mg/L)",
        min_value=0.0,
        max_value=20.0,
        value=8.0,
        step=0.1
    )

    enviar = st.form_submit_button("Register sample")

if enviar:
    if not local.strip():
        st.warning("Please enter a sample location.")
    else:
        nova_amostra = pd.DataFrame([{
            "Local": local.strip(),
            "pH": ph,
            "Temperatura (°C)": temperatura,
            "Oxigênio (mg/L)": oxigenio
        }])

        st.session_state.amostras = pd.concat(
            [st.session_state.amostras, nova_amostra],
            ignore_index=True
        )

        st.success("Sample added to the current session.")
        st.rerun()

# Tabela
st.header("Sample Records")
st.dataframe(
    st.session_state.amostras,
    use_container_width=True,
    hide_index=True
)

# Exportação CSV
csv = st.session_state.amostras.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="biowater_samples.csv",
    mime="text/csv"
)

st.caption(
    "BioWater | Educational environmental monitoring project"
)
