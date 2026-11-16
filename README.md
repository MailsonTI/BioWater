
# BioWater — Water Quality Monitoring Dashboard

## Overview

BioWater is an environmental monitoring and water quality analysis application developed to integrate Environmental Science and Information Technology.

The application allows users to register water samples, analyze measurements, monitor environmental indicators, visualize data through interactive charts, and manage historical records.

BioWater supports Portuguese and English interfaces, as well as SI and US temperature unit settings.

## Features

- Register water samples by location.
- Record pH, temperature, dissolved oxygen, turbidity, and electrical conductivity.
- Register sampling date and time.
- Display environmental indicators and statistics.
- Visualize measurements through interactive charts.
- Import sample data from CSV files.
- Export historical records to CSV.
- Store and manage records using SQLite.
- Archive and restore sample records.
- Support Portuguese and English interfaces.
- Support SI and US temperature units.

## Technologies Used

- **Python** — Main programming language.
- **Streamlit** — Interactive web application framework.
- **Pandas** — Data processing and analysis.
- **SQLite** — Relational database for sample storage.
- **Git** — Version control.
- **GitHub** — Source code hosting and project collaboration.

## Getting Started

### Prerequisites

- Python installed and available in your terminal.
- Git installed if you want to clone the repository.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/MailsonTI/BioWater.git
cd BioWater
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Project Structure

```text
BioWater/
│
├── app.py
├── database.py
├── water_analysis.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Main Files

- `app.py` — Main Streamlit application.
- `database.py` — SQLite database operations.
- `water_analysis.py` — Water quality analysis functions.
- `requirements.txt` — Python dependencies.
- `biowater.db` — Local SQLite database file, excluded from Git.

## Data and Limitations

The built-in measurements are simulated examples for learning. They are not real environmental observations and must not be used for public health or regulatory decisions.

The measurement ranges in the app are input-validation limits, not regulatory water-quality thresholds. Any future water-quality classification should use documented, authoritative references.

Sample records are stored locally in `biowater.db`. This database file is excluded from Git so local records are not included in the repository.

CSV duplicate prevention applies during the current Streamlit session.

## Project Goals

- Practice Python programming and data analysis with Pandas.
- Build an interactive dashboard with Streamlit.
- Explore how software can support environmental data review.
- Present a portfolio project combining science and information technology.

## Future Improvements

- Add water-quality reference ranges with documented sources.
- Expand data validation and reporting.

## About the Developer

**Mailson Maciel de Freitas**

Python Developer | Environmental Science & Technology

Background in Biology and Systems Analysis and Development.

BioWater represents the integration of scientific knowledge and software development to support environmental monitoring and water quality analysis.

## Project Status

BioWater is an ongoing project. New features, improvements, and refinements may be introduced as development progresses.

## License

This project is currently available for portfolio and educational purposes. No open-source license has been specified.