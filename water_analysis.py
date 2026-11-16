def analyze_water(
    ph,
    temperature,
    dissolved_oxygen,
    turbidity,
    conductivity,
    language="pt"
):

    results = []

    is_en = language == "en"

    # pH
    if 6.0 <= ph <= 9.0:
        status = "Adequate" if is_en else "Adequado"
        color = "green"
    else:
        status = (
            "Outside reference range"
            if is_en else "Fora da referência"
        )
        color = "red"

    results.append({
        "parameter": "pH",
        "value": ph,
        "status": status,
        "color": color
    })

    # Temperature
    if 0 <= temperature <= 30:
        status = "Acceptable" if is_en else "Adequada"
        color = "green"
    else:
        status = (
            "Outside reference range"
            if is_en else "Fora da referência"
        )
        color = "red"

    results.append({
        "parameter": "Temperature" if is_en else "Temperatura",
        "value": temperature,
        "status": status,
        "color": color
    })

    # Dissolved oxygen
    if dissolved_oxygen >= 5:
        status = "Adequate" if is_en else "Adequado"
        color = "green"
    else:
        status = (
            "Below reference range"
            if is_en else "Abaixo da referência"
        )
        color = "red"

    results.append({
        "parameter": (
            "Dissolved oxygen"
            if is_en else "Oxigênio dissolvido"
        ),
        "value": dissolved_oxygen,
        "status": status,
        "color": color
    })

    # Turbidity
    results.append({
        "parameter": "Turbidity" if is_en else "Turbidez",
        "value": f"{turbidity:.2f} NTU",
        "status": (
            "Recorded — requires specific reference"
            if is_en else
            "Registrada — requer referência específica"
        ),
        "color": "blue"
    })

    # Electrical Conductivity
    results.append({
        "parameter": (
            "Electrical conductivity"
            if is_en else "Condutividade elétrica"
        ),
        "value": f"{conductivity:.2f} µS/cm",
        "status": (
            "Recorded — requires specific reference"
            if is_en else
            "Registrada — requer referência específica"
        ),
        "color": "blue"
    })

    return results