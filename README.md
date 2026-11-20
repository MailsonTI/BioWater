# BioWater — Water Quality Monitoring Dashboard

BioWater is a bilingual dashboard for recording and reviewing water quality measurements. It brings together environmental data and software in a practical portfolio project.

**Languages:** Portuguese and English<br>
**Units:** SI and US temperature settings

## Features

- Record sample location, date and time, pH, temperature, dissolved oxygen, turbidity, and electrical conductivity.
- Review environmental indicators, summary statistics, and interactive charts.
- Browse measurement history and archive or restore records.
- Import and export sample records as CSV.
- Store records locally in SQLite.
- Switch the interface between Portuguese and English.

## Run locally

### Requirements

- Python 3.10 or newer
- Git (to clone the repository)

### Setup

```bash
git clone https://github.com/MailsonTI/BioWater.git
cd BioWater
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Install dependencies and start the dashboard:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser. On first run, it creates a local `biowater.db` SQLite database.

## Project structure

```text
BioWater/
├── app.py              # Streamlit interface
├── database.py         # SQLite storage and record management
├── water_analysis.py   # Measurement analysis functions
├── requirements.txt    # Python dependencies
└── README.md
```

## Data and limitations

The sample records included for demonstration are simulated. They are not field observations and must not be used for public health, drinking-water, or regulatory decisions. The app's measurement limits are input-validation boundaries, not water-quality standards. Any future classification should cite appropriate authoritative sources.

Records are stored locally in `biowater.db`, which is excluded from Git. Each user gets a separate local database. CSV duplicate prevention applies only during the current app session.

## Development status

BioWater is an ongoing educational and portfolio project. Current areas for improvement include sourced water-quality reference ranges and broader validation and reporting.

## About

**Mailson Maciel de Freitas**<br>
Python Developer | Environmental Science & Technology<br>
Background in Biology and Systems Analysis and Development.

## License

The project is shared for portfolio and educational purposes. No open-source license has been specified.

---

# BioWater — Painel de Monitoramento da Qualidade da Água

O BioWater é um painel bilíngue para registrar e analisar medições da qualidade da água. O projeto combina dados ambientais e desenvolvimento de software em uma aplicação prática para portfólio.

**Idiomas:** português e inglês<br>
**Unidades:** configurações SI e US para temperatura

## Funcionalidades

- Registrar local, data e hora da coleta, pH, temperatura, oxigênio dissolvido, turbidez e condutividade elétrica.
- Consultar indicadores ambientais, estatísticas resumidas e gráficos interativos.
- Navegar pelo histórico e arquivar ou restaurar registros.
- Importar e exportar registros em CSV.
- Armazenar os registros localmente em SQLite.
- Alternar a interface entre português e inglês.

## Executar localmente

### Requisitos

- Python 3.10 ou superior
- Git (para clonar o repositório)

### Configuração

```bash
git clone https://github.com/MailsonTI/BioWater.git
cd BioWater
python -m venv .venv
```

Ative o ambiente:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

Instale as dependências e inicie o painel:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

O app será aberto no navegador. Na primeira execução, ele cria o banco SQLite local `biowater.db`.

## Estrutura do projeto

```text
BioWater/
├── app.py              # Interface Streamlit
├── database.py         # Armazenamento SQLite e gerenciamento dos registros
├── water_analysis.py   # Funções de análise das medições
├── requirements.txt    # Dependências Python
└── README.md
```

## Dados e limitações

Os registros incluídos para demonstração são simulados. Eles não são observações de campo e não devem ser usados em decisões de saúde pública, potabilidade ou conformidade regulatória. Os limites de medição do app servem para validar entradas, não são padrões de qualidade da água. Uma classificação futura deve citar fontes oficiais apropriadas.

Os registros ficam armazenados localmente em `biowater.db`, arquivo excluído do Git. Cada usuário mantém seu próprio banco local. A prevenção de duplicatas na importação CSV vale apenas durante a sessão atual do app.

## Status do desenvolvimento

O BioWater é um projeto educacional e de portfólio em andamento. Entre as melhorias previstas estão faixas de referência da qualidade da água com fontes documentadas e validações e relatórios mais abrangentes.

## Sobre

**Mailson Maciel de Freitas**<br>
Desenvolvedor Python | Ciências Ambientais e Tecnologia<br>
Formação em Biologia e Análise e Desenvolvimento de Sistemas.

## Licença

O projeto está disponível para fins de portfólio e educação. Nenhuma licença de código aberto foi especificada.
