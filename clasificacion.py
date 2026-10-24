import unicodedata

PALABRAS_CLAVE = {
    "CRITICO": ["colaps", "derrumb", "inhabitable", "destruid", "desplom",
                "perdida total", "arrasad", "se cayo la casa", "se cayo la vivienda"],
    "ALTO": ["columna", "viga", "techo", "muro caido", "pared caida", "cimiento",
             "lodo", "inundad", "socavad", "inclinad", "cerco"],
    "MODERADO": ["grieta", "fisura", "rajadura", "humedad", "filtracion"],
}


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def clasificar_dano(descripcion):
    texto = normalizar(descripcion)
    for nivel in ["CRITICO", "ALTO", "MODERADO"]:
        for palabra in PALABRAS_CLAVE[nivel]:
            if palabra in texto:
                return nivel
    return "LEVE"