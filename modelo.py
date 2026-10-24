TIPOS_DESASTRE = ["HUAICO", "INUNDACION", "TERREMOTO"]
ESTADOS = ["PENDIENTE", "EVALUACION PROGRAMADA", "ATENDIDO", "OBSERVADO"]
NIVELES = ["CRITICO", "ALTO", "MODERADO", "LEVE"]

PRIORIDAD = {"CRITICO": 4, "ALTO": 3, "MODERADO": 2, "LEVE": 1}

TRANSICIONES = {
    "PENDIENTE": ["EVALUACION PROGRAMADA", "OBSERVADO"],
    "OBSERVADO": ["PENDIENTE"],
    "EVALUACION PROGRAMADA": ["ATENDIDO", "OBSERVADO"],
    "ATENDIDO": [],
}


def crear_solicitud(codigo, datos, nivel, fecha_registro):
    return {
        "codigo": codigo,
        "dni": datos["dni"],
        "nombres": datos["nombres"],
        "telefono": datos["telefono"],
        "direccion": datos["direccion"],
        "sector": datos["sector"],
        "tipo": datos["tipo"],
        "fecha_desastre": datos["fecha_desastre"],
        "descripcion": datos["descripcion"],
        "nivel": nivel,
        "estado": "PENDIENTE",
        "observacion": "",
        "fecha_registro": fecha_registro,
    }