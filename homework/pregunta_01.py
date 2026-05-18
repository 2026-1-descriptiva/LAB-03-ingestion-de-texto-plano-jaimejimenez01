"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import re
    import pandas as pd

    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip headers: find the separator line (all dashes)
    data_start = 0
    for i, line in enumerate(lines):
        if line.strip() and all(c == "-" for c in line.strip()):
            data_start = i + 1
            break

    # Fixed-width column positions (0-indexed)
    # cluster: 0-8, cantidad: 9-24, porcentaje: 25-39, keywords: 40+
    KEYWORDS_START = 40

    records = []
    current_meta = None
    current_keywords = []

    for line in lines[data_start:]:
        padded = line.rstrip("\n").ljust(80)

        cluster_str = padded[0:9].strip()
        cantidad_str = padded[9:25].strip()
        porcentaje_str = padded[25:40].strip()
        keywords_part = padded[KEYWORDS_START:].rstrip()

        if cluster_str.isdigit():
            # Save previous cluster
            if current_meta is not None:
                kw = " ".join(p.strip() for p in current_keywords if p.strip())
                kw = re.sub(r" +", " ", kw).rstrip(".").strip()
                records.append({**current_meta, "principales_palabras_clave": kw})

            pct = float(porcentaje_str.replace(" %", "").replace(",", "."))
            current_meta = {
                "cluster": int(cluster_str),
                "cantidad_de_palabras_clave": int(cantidad_str),
                "porcentaje_de_palabras_clave": pct,
            }
            current_keywords = [keywords_part]

        elif current_meta is not None and keywords_part.strip():
            current_keywords.append(keywords_part)

    # Save last cluster
    if current_meta is not None:
        kw = " ".join(p.strip() for p in current_keywords if p.strip())
        kw = re.sub(r" +", " ", kw).rstrip(".").strip()
        records.append({**current_meta, "principales_palabras_clave": kw})

    return pd.DataFrame(records)
