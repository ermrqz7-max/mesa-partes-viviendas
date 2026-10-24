"""CSV en UTF-8 con reemplazo atómico e historial dentro de cada registro."""
import csv
from datetime import datetime
import json
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile

from modelo import ESTADOS, NIVELES, TIPOS_DESASTRE
from validacion import validar_solicitud

CAMPOS_BASE = ["codigo", "dni", "nombres", "telefono", "direccion", "sector",
               "tipo", "fecha_desastre", "descripcion", "nivel", "estado",
               "observacion", "fecha_registro"]
CAMPOS = CAMPOS_BASE + ["historial"]
RUTA = Path(__file__).resolve().parent / "datos" / "solicitudes.csv"


def guardar(solicitudes, ruta=RUTA):
    """Solo reemplaza el CSV anterior cuando termina de escribir el nuevo."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with NamedTemporaryFile(mode="w", newline="", encoding="utf-8",
                                dir=ruta.parent, prefix="solicitudes_",
                                suffix=".tmp", delete=False) as archivo:
            temporal = Path(archivo.name)
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            for solicitud in solicitudes:
                fila = dict(solicitud)
                fila["historial"] = json.dumps(fila.get("historial", []),
                                               ensure_ascii=False)
                escritor.writerow(fila)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()


def cargar(ruta=RUTA):
    """Un archivo ausente inicia vacío; uno inválido genera un error explícito."""
    try:
        archivo = open(ruta, "r", newline="", encoding="utf-8")
    except FileNotFoundError:
        return []
    with archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames not in [CAMPOS_BASE, CAMPOS]:
            raise ValueError("El CSV no tiene las columnas esperadas.")
        solicitudes = []
        codigos = set()
        for numero, fila in enumerate(lector, start=2):
            if None in fila or any(valor is None for valor in fila.values()):
                raise ValueError(f"Fila {numero}: cantidad de columnas incorrecta.")
            if validar_solicitud(fila):
                raise ValueError(f"Fila {numero}: datos de solicitud no válidos.")
            if not re.fullmatch(r"MPV-[0-9]{4}-[0-9]{4}", fila["codigo"]):
                raise ValueError(f"Fila {numero}: código no válido.")
            if fila["codigo"] in codigos:
                raise ValueError(f"Fila {numero}: código repetido.")
            if (fila["nivel"] not in NIVELES or fila["estado"] not in ESTADOS
                    or fila["tipo"] not in TIPOS_DESASTRE):
                raise ValueError(f"Fila {numero}: categoría no válida.")
            try:
                datetime.strptime(fila["fecha_registro"], "%Y-%m-%d %H:%M:%S")
                historial = json.loads(fila.get("historial", "[]") or "[]")
                if not isinstance(historial, list):
                    raise ValueError("Historial no es lista")
                for cambio in historial:
                    if (not isinstance(cambio, dict)
                            or cambio.get("estado") not in ESTADOS
                            or not isinstance(cambio.get("observacion"), str)):
                        raise ValueError("Movimiento no válido")
                    datetime.strptime(cambio["fecha"], "%Y-%m-%d %H:%M:%S")
                if historial and historial[-1]["estado"] != fila["estado"]:
                    raise ValueError("Historial y estado no coinciden")
            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(f"Fila {numero}: fecha o historial no válido.") from error
            fila["historial"] = historial
            codigos.add(fila["codigo"])
            solicitudes.append(fila)
        return solicitudes
