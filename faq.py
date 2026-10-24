from clasificacion import normalizar

PLAZOS = {
    "CRITICO": "24 a 72 horas",
    "ALTO": "3 a 5 días hábiles",
    "MODERADO": "5 a 10 días hábiles",
    "LEVE": "10 a 15 días hábiles",
}

PREGUNTAS = [
    {"pregunta": "¿Qué datos necesito para registrar mi solicitud?",
     "respuesta": "DNI, nombres y apellidos, celular, dirección de la vivienda, sector, tipo y fecha del desastre y una descripción del daño.",
     "claves": ["dato", "necesito", "requisito", "documento"]},
    {"pregunta": "¿Cómo sé que mi solicitud fue registrada?",
     "respuesta": "El sistema muestra una constancia con tu código de seguimiento y el nivel preliminar.",
     "claves": ["registrada", "constancia", "confirmacion"]},
    {"pregunta": "¿Qué es el código de seguimiento?",
     "respuesta": "Es un código único con formato MPV-AAAA-NNNN. Con él consultas el estado de tu trámite.",
     "claves": ["codigo", "seguimiento", "mpv"]},
    {"pregunta": "¿Cómo consulto el estado de mi trámite?",
     "respuesta": "Usa la opción Consultar con tu código o con tu DNI.",
     "claves": ["consultar", "estado", "tramite"]},
    {"pregunta": "¿Qué significa el nivel de daño preliminar?",
     "respuesta": "Es una clasificación automática (CRÍTICO, ALTO, MODERADO o LEVE) según lo que describiste. Sirve para ordenar la atención.",
     "claves": ["nivel", "preliminar", "clasificacion", "dano"]},
    {"pregunta": "¿La clasificación reemplaza la evaluación técnica?",
     "respuesta": "No. La evaluación real la hace el personal técnico competente (EDAN).",
     "claves": ["reemplaza", "edan", "tecnica", "evaluacion"]},
    {"pregunta": "¿Cuánto demora la visita técnica?",
     "respuesta": "Depende del nivel. Los plazos son referenciales: crítico 24 a 72 horas, alto 3 a 5 días hábiles, moderado 5 a 10 y leve 10 a 15.",
     "claves": ["demora", "plazo", "cuanto", "visita", "tiempo"]},
    {"pregunta": "¿Qué hago si ya registré mi vivienda?",
     "respuesta": "No la registres de nuevo. Si lo intentas, el sistema te mostrará el código de la solicitud existente.",
     "claves": ["duplicado", "repetido", "ya registre", "dos veces"]},
    {"pregunta": "¿Puede un familiar registrar la misma vivienda?",
     "respuesta": "No. Una vivienda tiene una sola solicitud por evento, sin importar quién la registre.",
     "claves": ["familiar", "vecino", "otra persona"]},
    {"pregunta": "¿Qué significa el estado PENDIENTE?",
     "respuesta": "Tu solicitud fue registrada y aún no tiene visita técnica programada.",
     "claves": ["pendiente"]},
    {"pregunta": "¿Qué significa OBSERVADO y qué debo hacer?",
     "respuesta": "Falta un dato o no se pudo ubicar la vivienda. Debes subsanar la observación para que vuelva a PENDIENTE.",
     "claves": ["observado", "subsanar", "falta"]},
    {"pregunta": "¿Qué significa EVALUACIÓN PROGRAMADA?",
     "respuesta": "Ya se agendó la visita técnica a tu vivienda.",
     "claves": ["programada", "programacion", "agendada"]},
    {"pregunta": "¿Qué pasa cuando mi solicitud figura como ATENDIDO?",
     "respuesta": "Se realizó la evaluación técnica y la solicitud sale de la bandeja de revisión.",
     "claves": ["atendido", "finalizado", "cerrado"]},
    {"pregunta": "¿Qué tipos de desastre se pueden registrar?",
     "respuesta": "Huaico, inundación o terremoto.",
     "claves": ["tipo", "desastre", "huaico", "inundacion", "terremoto", "sismo"]},
]


def plazo_por_nivel(nivel):
    return PLAZOS.get(nivel, "No definido")


def obtener_respuesta(indice):
    if 0 <= indice < len(PREGUNTAS):
        return PREGUNTAS[indice]["respuesta"]
    return None


def buscar_preguntas(texto):
    consulta = normalizar(texto)
    resultado = []
    for i in range(len(PREGUNTAS)):
        puntos = 0
        for clave in PREGUNTAS[i]["claves"]:
            if clave in consulta:
                puntos += 2
        if puntos > 0:
            resultado.append([i, puntos])
    for k in range(1, len(resultado)):
        actual = resultado[k]
        j = k - 1
        while j >= 0 and resultado[j][1] < actual[1]:
            resultado[j + 1] = resultado[j]
            j = j - 1
        resultado[j + 1] = actual
    return resultado[:3]