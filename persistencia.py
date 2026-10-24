import csv
import os

CAMPOS = ["codigo", "dni", "nombres", "telefono", "direccion", "sector",
          "tipo", "fecha_desastre", "descripcion", "nivel", "estado",
          "observacion", "fecha_registro"]
RUTA = "datos/solicitudes.csv"


def guardar(solicitudes, ruta=RUTA):
    carpeta = os.path.dirname(ruta)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for s in solicitudes:
            escritor.writerow(s)


def cargar(ruta=RUTA):
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        return []