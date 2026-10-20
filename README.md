
# BioWater — Water Quality Monitoring Dashboard

## Overview

BioWater is an educational environmental monitoring project that demonstrates how Python and data visualization can support the analysis of water quality measurements.

The application provides a simple dashboard for recording sample measurements, viewing key indicators, visualizing data, and exporting records to CSV.

## Features

- Register water samples by location.
- Record pH, temperature, and dissolved oxygen.
- Display summary indicators.
- Visualize measurements in a chart.
- View sample records in a table.
- Export sample data to a CSV file.

## Technologies

- Python
- Streamlit
- Pandas
- Git and GitHub

## Getting Started

### Prerequisites

- Python installed on your computer.
- Git installed if you want to clone the repository.

### Installation

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Open the project directory:

   ```bash
   cd BioWater
   ```

3. Create and activate a virtual environment.

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, you can use Command Prompt:

   ```bat
   .venv\Scripts\activate.bat
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

## Data Notice

The initial measurements are simulated examples for demonstration and learning purposes. They are not real environmental observations and should not be used to make public health or regulatory decisions.

Sample records are held in the current Streamlit session. They are not permanently stored by the application.

## Project Goals

- Practice Python programming.
- Explore data analysis with Pandas.
- Build an interactive dashboard with Streamlit.
- Present environmental data in a clear, accessible format.
- Develop a portfolio project combining science and information technology.

## Future Improvements

- Add persistent data storage.
- Import datasets from CSV files.
- Add water quality reference ranges with documented sources.
- Improve data validation and reporting.

## Author

Created as a learning and portfolio project in environmental data analysis and software development.
